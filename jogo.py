import pygame
import constants
from tabuleiro import Tabuleiro
from botao import Botao
from jogador import JogadorLogico, JogadorAleatorio

class Jogo:
    def __init__(self):
        self.linhas = 15
        self.colunas = 15
        self.num_bombas = 38

        self.relogio = pygame.time.Clock()

        self.botao_facil = Botao(10, 10, 100, 40, "Fácil")
        self.botao_medio = Botao(120, 10, 100, 40, "Médio")
        self.botao_dificil = Botao(230, 10, 100, 40, "Difícil")

        self.reiniciar()

    def reiniciar(self):
        self.largura_tabuleiro = self.colunas * constants.TAMANHO_CELULA
        self.largura_tela = (self.largura_tabuleiro * 2) + constants.ESPACO_MEIO
        self.altura_tela = (self.linhas * constants.TAMANHO_CELULA) + constants.ALTURA_MENU

        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption("Campo Minado - Batalha com Pontuação")

        largura_botao = 160
        pos_x_botao = (self.largura_tela - largura_botao) // 2
        self.botao_reiniciar = Botao(pos_x_botao, 10, largura_botao, 40, "Nova Batalha")

        self.tab_logico = Tabuleiro(self.linhas, self.colunas, self.num_bombas, gerar_bombas=True)

        self.tab_random = Tabuleiro(self.linhas, self.colunas, self.num_bombas, gerar_bombas=False)
        self.tab_random.clonar_de(self.tab_logico)

        self.jog_logico = JogadorLogico(self.tab_logico)
        self.jog_random = JogadorAleatorio(self.tab_random)

        self.estado_logico = "JOGANDO"
        self.estado_random = "JOGANDO"
        self.timer_ia = 0

    def definir_dificuldade(self, linhas, colunas, num_bombas):
        self.linhas = linhas
        self.colunas = colunas
        self.num_bombas = num_bombas
        self.reiniciar()

    def processar_clique(self, pos, botao_mouse):
        if botao_mouse == 1:
            if self.botao_reiniciar.foi_clicado(pos):
                self.reiniciar()
            elif self.botao_facil.foi_clicado(pos):
                self.definir_dificuldade(10, 10, 15)
            elif self.botao_medio.foi_clicado(pos):
                self.definir_dificuldade(15, 15, 38)
            elif self.botao_dificil.foi_clicado(pos):
                self.definir_dificuldade(20, 20, 80)

    '''Modificar para que rodar sem interface'''
    def desenhar_interface(self):
        self.tela.fill(constants.COR_FUNDO)
        self.botao_reiniciar.desenhar(self.tela)
        self.botao_facil.desenhar(self.tela)
        self.botao_medio.desenhar(self.tela)
        self.botao_dificil.desenhar(self.tela)

        centro_l = self.largura_tabuleiro // 2
        centro_r = self.largura_tabuleiro + constants.ESPACO_MEIO + (self.largura_tabuleiro // 2)

        texto_l = constants.FONTE_TITULOS.render("IA LÓGICA", True, constants.COR_LOGICO)
        texto_r = constants.FONTE_TITULOS.render("IA ALEATÓRIA", True, constants.COR_RANDOM)
        self.tela.blit(texto_l, texto_l.get_rect(center=(centro_l, 65)))
        self.tela.blit(texto_r, texto_r.get_rect(center=(centro_r, 65)))

        pts_l = self.tab_logico.obter_pontuacao()
        pts_r = self.tab_random.obter_pontuacao()
        score_l = constants.FONTE_PLACARES.render(f"Pontos: {pts_l}", True, constants.COR_TEXTO)
        score_r = constants.FONTE_PLACARES.render(f"Pontos: {pts_r}", True, constants.COR_TEXTO)
        self.tela.blit(score_l, score_l.get_rect(center=(centro_l, 90)))
        self.tela.blit(score_r, score_r.get_rect(center=(centro_r, 90)))

        if self.estado_logico != "JOGANDO":
            cor = constants.COR_VITORIA if self.estado_logico == "VENCEU" else constants.COR_BOMBA
            status_l = constants.FONTE_PLACARES.render(self.estado_logico, True, cor)
            self.tela.blit(status_l, status_l.get_rect(center=(centro_l, 115)))

        if self.estado_random != "JOGANDO":
            cor = constants.COR_VITORIA if self.estado_random == "VENCEU" else constants.COR_BOMBA
            status_r = constants.FONTE_PLACARES.render(self.estado_random, True, cor)
            self.tela.blit(status_r, status_r.get_rect(center=(centro_r, 115)))

        if self.estado_logico != "JOGANDO" and self.estado_random != "JOGANDO":
            if pts_l > pts_r:
                vencedor_txt = "A LÓGICA VENCEU!"
                cor_v = constants.COR_LOGICO
            elif pts_r > pts_l:
                vencedor_txt = "A SORTE VENCEU!"
                cor_v = constants.COR_RANDOM
            else:
                vencedor_txt = "EMPATE!"
                cor_v = constants.COR_TEXTO

            txt_final = constants.FONTE_VENCEDOR.render(vencedor_txt, True, cor_v)
            self.tela.blit(txt_final, txt_final.get_rect(center=(self.largura_tela // 2, 115)))

    def rodar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.processar_clique(pygame.mouse.get_pos(), evento.button)

            self.timer_ia += 1
            if self.timer_ia >= 10:
                self.timer_ia = 0

                if self.estado_logico == "JOGANDO":
                    acao, l, c = self.jog_logico.realizar_jogada()
                    if acao == "CLICAR":
                        if self.tab_logico.revelar(l, c):
                            self.estado_logico = "PERDEU"
                            self.tab_logico.revelar_todas_bombas()
                        elif self.tab_logico.verificar_vitoria():
                            self.estado_logico = "VENCEU"

                if self.estado_random == "JOGANDO":
                    acao, l, c = self.jog_random.realizar_jogada()
                    if acao == "CLICAR":
                        if self.tab_random.revelar(l, c):
                            self.estado_random = "PERDEU"
                            self.tab_random.revelar_todas_bombas()
                        elif self.tab_random.verificar_vitoria():
                            self.estado_random = "VENCEU"

            self.desenhar_interface()

            self.tab_logico.desenhar(self.tela, offset_x=0)
            offset_r = self.largura_tabuleiro + constants.ESPACO_MEIO
            self.tab_random.desenhar(self.tela, offset_x=offset_r)

            pygame.display.flip()
            self.relogio.tick(30)
