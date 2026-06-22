import pygame
import constants
from tabuleiro import Tabuleiro
from botao import Botao
from jogador import JogadorLogico, JogadorAleatorio
from database import db, ResultadoSimulacao
from pony.orm import db_session, select
import time

class PartidaSimulacao:
    def __init__(self, linhas, colunas, num_bombas):
        self.linhas = linhas
        self.colunas = colunas
        self.num_bombas = num_bombas

        self.tab_logico = Tabuleiro(linhas, colunas, num_bombas, gerar_bombas=True)
        self.tab_random = Tabuleiro(linhas, colunas, num_bombas, gerar_bombas=False)
        self.tab_random.clonar_de(self.tab_logico)

        self.logico = JogadorLogico(self.tab_logico)
        self.random = JogadorAleatorio(self.tab_random)

        self.estado_l = "JOGANDO"
        self.estado_r = "JOGANDO"

    def jogar_turno(self):
        jogou = False
        if self.estado_l == "JOGANDO":
            acao, l, c = self.logico.realizar_jogada()
            if acao == "CLICAR":
                if self.tab_logico.revelar(l, c):
                    self.estado_l = "PERDEU"
                elif self.tab_logico.verificar_vitoria():
                    self.estado_l = "VENCEU"
            elif acao == "TRAVOU":
                self.estado_l = "PERDEU"
            jogou = True

        if self.estado_r == "JOGANDO":
            acao, l, c = self.random.realizar_jogada()
            if acao == "CLICAR":
                if self.tab_random.revelar(l, c):
                    self.estado_r = "PERDEU"
                elif self.tab_random.verificar_vitoria():
                    self.estado_r = "VENCEU"
            elif acao == "TRAVOU":
                self.estado_r = "PERDEU"
            jogou = True

        return self.estado_l != "JOGANDO" and self.estado_r != "JOGANDO"


class TestadorDeMapasVisual:
    def __init__(self, quantidade=1000):
        pygame.init()

        self.largura_tela = (20 * constants.TAMANHO_CELULA * 2) + constants.ESPACO_MEIO
        self.altura_tela = (20 * constants.TAMANHO_CELULA) + constants.ALTURA_MENU

        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption("Simulação em Lote - Pygame")
        self.relogio = pygame.time.Clock()

        self.quantidade_total = quantidade
        self.mapas_config = [
            {"nome": "Espaçado", "l": 15, "c": 15, "b": 10},
            {"nome": "Mediano", "l": 15, "c": 15, "b": 38},
            {"nome": "Denso", "l": 15, "c": 15, "b": 70},
            {"nome": "Pequeno", "l": 10, "c": 10, "b": 15},
            {"nome": "Grande", "l": 20, "c": 20, "b": 80}
        ]
        self.mapa_index = 0
        self.partidas_concluidas = 0

        self.vitorias_logico = 0
        self.vitorias_random = 0
        self.empates = 0
        self.pontos_logico = 0
        self.pontos_random = 0

        self.partida_atual = None
        self.iniciar_proxima_partida()

        self.visual_ligado = False
        self.pausado = False

        self.btn_visual = Botao(10, 10, 150, 40, "Ver: OFF")
        self.btn_pausa = Botao(170, 10, 150, 40, "Pausar")

    def iniciar_proxima_partida(self):
        conf = self.mapas_config[self.mapa_index]
        self.partida_atual = PartidaSimulacao(conf["l"], conf["c"], conf["b"])

    @db_session
    def _salvar_resultado_banco(self):
        conf = self.mapas_config[self.mapa_index]
        ResultadoSimulacao(
            tipo_mapa=conf["nome"],
            linhas=conf["l"],
            colunas=conf["c"],
            num_bombas=conf["b"],
            vitorias_logico=self.vitorias_logico,
            vitorias_random=self.vitorias_random,
            empates=self.empates,
            pontos_logico=self.pontos_logico,
            pontos_random=self.pontos_random,
            quantidade_partidas=self.quantidade_total
        )

    def processar_clique(self, pos, botao_mouse):
        if botao_mouse == 1:
            if self.btn_visual.foi_clicado(pos):
                self.visual_ligado = not self.visual_ligado
                self.btn_visual.texto = "Ver: ON" if self.visual_ligado else "Ver: OFF"
            elif self.btn_pausa.foi_clicado(pos):
                self.pausado = not self.pausado
                self.btn_pausa.texto = "Retomar" if self.pausado else "Pausar"

    def avancar_mapa(self):
        self._salvar_resultado_banco()

        self.mapa_index += 1
        self.partidas_concluidas = 0
        self.vitorias_logico = 0
        self.vitorias_random = 0
        self.empates = 0
        self.pontos_logico = 0
        self.pontos_random = 0

        if self.mapa_index < len(self.mapas_config):
            self.iniciar_proxima_partida()

    def processar_partida_ate_o_fim(self):
        while True:
            acabou = self.partida_atual.jogar_turno()
            if acabou:
                pts_l = self.partida_atual.tab_logico.obter_pontuacao()
                pts_r = self.partida_atual.tab_random.obter_pontuacao()
                self.pontos_logico += pts_l
                self.pontos_random += pts_r

                if pts_l > pts_r:
                    self.vitorias_logico += 1
                elif pts_r > pts_l:
                    self.vitorias_random += 1
                else:
                    self.empates += 1

                self.partidas_concluidas += 1
                break

    @db_session
    def desenhar_tela_resultados(self):
        txt_titulo = constants.FONTE_VENCEDOR.render("BATERIA DE TESTES FINALIZADA! RESULTADOS:", True, constants.COR_VITORIA)
        self.tela.blit(txt_titulo, txt_titulo.get_rect(center=(self.largura_tela // 2, 50)))

        cabecalho = ["ID", "Mapa", "Tamanho", "Bombas", "Vit. Lógico", "Vit. Random", "Pts Lógico", "Pts Random"]

        y_pos = 120
        x_colunas = [20, 80, 250, 420, 560, 720, 880, 1040]

        for i, texto in enumerate(cabecalho):
            txt_cab = constants.FONTE_TITULOS.render(texto, True, constants.COR_LOGICO)
            self.tela.blit(txt_cab, (x_colunas[i], y_pos))

        y_pos += 40

        resultados = select(r for r in ResultadoSimulacao).order_by(ResultadoSimulacao.id)[:]

        for r in resultados:
            if y_pos > self.altura_tela - 50:
                break

            linha_str = [
                str(r.id),
                r.tipo_mapa,
                f"{r.linhas}x{r.colunas}",
                str(r.num_bombas),
                str(r.vitorias_logico),
                str(r.vitorias_random),
                str(r.pontos_logico),
                str(r.pontos_random)
            ]

            for i, texto in enumerate(linha_str):
                txt_linha = constants.FONTE_PLACARES.render(texto, True, constants.COR_TEXTO)
                self.tela.blit(txt_linha, (x_colunas[i], y_pos))

            y_pos += 30

    def desenhar_painel_progresso(self):
        self.tela.fill(constants.COR_FUNDO)

        if self.mapa_index >= len(self.mapas_config):
            self.desenhar_tela_resultados()
            return

        self.btn_visual.desenhar(self.tela)
        self.btn_pausa.desenhar(self.tela)

        conf = self.mapas_config[self.mapa_index]

        txt_mapa = constants.FONTE_TITULOS.render(f"Processando Mapa: {conf['nome']} ({conf['l']}x{conf['c']}, {conf['b']} bombas)", True, constants.COR_TEXTO)
        self.tela.blit(txt_mapa, (10, 80))

        progresso = f"{self.partidas_concluidas} / {self.quantidade_total} Partidas"
        txt_progresso = constants.FONTE_TITULOS.render(progresso, True, constants.COR_TEXTO)
        self.tela.blit(txt_progresso, (10, 110))

        largura_barra = 400
        altura_barra = 20
        x_barra = 10
        y_barra = 140
        pygame.draw.rect(self.tela, constants.COR_LINHA, (x_barra, y_barra, largura_barra, altura_barra), 2)

        preenchimento = int((self.partidas_concluidas / self.quantidade_total) * largura_barra)
        pygame.draw.rect(self.tela, constants.COR_VITORIA, (x_barra, y_barra, preenchimento, altura_barra))

    def desenhar_jogo_ativo(self):
        centro_l = self.largura_tela // 4
        centro_r = (self.largura_tela // 4) * 3

        largura_tab = self.partida_atual.colunas * constants.TAMANHO_CELULA
        altura_tab = self.partida_atual.linhas * constants.TAMANHO_CELULA

        offset_x_l = centro_l - (largura_tab // 2)
        offset_x_r = centro_r - (largura_tab // 2)

        area_restante_y = self.altura_tela - constants.ALTURA_MENU
        offset_y = constants.ALTURA_MENU + (area_restante_y - altura_tab) // 2

        self.partida_atual.tab_logico.desenhar(self.tela, offset_x=offset_x_l, offset_y=offset_y)
        self.partida_atual.tab_random.desenhar(self.tela, offset_x=offset_x_r, offset_y=offset_y)

    def rodar(self):
        rodando = True
        timer = 0
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.processar_clique(pygame.mouse.get_pos(), evento.button)

            if self.mapa_index < len(self.mapas_config):
                if not self.pausado:
                    if self.visual_ligado:
                        timer += 1
                        if timer >= 5:
                            timer = 0
                            acabou = self.partida_atual.jogar_turno()
                            if acabou:
                                pts_l = self.partida_atual.tab_logico.obter_pontuacao()
                                pts_r = self.partida_atual.tab_random.obter_pontuacao()
                                self.pontos_logico += pts_l
                                self.pontos_random += pts_r

                                if pts_l > pts_r:
                                    self.vitorias_logico += 1
                                elif pts_r > pts_l:
                                    self.vitorias_random += 1
                                else:
                                    self.empates += 1

                                self.partidas_concluidas += 1

                                if self.partidas_concluidas >= self.quantidade_total:
                                    self.avancar_mapa()
                                else:
                                    self.iniciar_proxima_partida()
                    else:
                        tempo_inicio = time.perf_counter()
                        while (time.perf_counter() - tempo_inicio) < 0.03: # 30ms
                            if self.partidas_concluidas >= self.quantidade_total:
                                self.avancar_mapa()
                                break
                            self.processar_partida_ate_o_fim()
                            self.iniciar_proxima_partida()

            self.desenhar_painel_progresso()

            if self.visual_ligado and self.mapa_index < len(self.mapas_config):
                self.desenhar_jogo_ativo()

            pygame.display.flip()
            self.relogio.tick(30)

        pygame.quit()


if __name__ == "__main__":
    testador = TestadorDeMapasVisual(quantidade=1000)
    testador.rodar()
