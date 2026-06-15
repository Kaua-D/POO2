import time
import constants
from tabuleiro import Tabuleiro
from jogador import JogadorLogico, JogadorAleatorio

def rodar_simulacao(quantidade, linhas=15, colunas=15, num_bombas=38):
    vitorias_logico = 0
    vitorias_random = 0
    empates = 0
    pontos_logico_total = 0
    pontos_random_total = 0


    print(f"Iniciando simulação de {quantidade} partidas ({linhas}x{colunas}, {num_bombas} bombas)...")
    print("Por favor, aguarde o processamento...\n")

    tempo_inicio = time.time()

    for i in range(quantidade):
        tab_logico = Tabuleiro(linhas, colunas, num_bombas, gerar_bombas=True)
        tab_random = Tabuleiro(linhas, colunas, num_bombas, gerar_bombas=False)
        tab_random.clonar_de(tab_logico)

        logico = JogadorLogico(tab_logico)
        random = JogadorAleatorio(tab_random)

        estado_l = "JOGANDO"
        while estado_l == "JOGANDO":
            acao, l, c = logico.realizar_jogada()
            if acao == "CLICAR":
                if tab_logico.revelar(l, c):
                    estado_l = "PERDEU"
                elif tab_logico.verificar_vitoria():
                    estado_l = "VENCEU"
            elif acao == "TRAVOU":
                break

        estado_r = "JOGANDO"
        while estado_r == "JOGANDO":
            acao, l, c = random.realizar_jogada()
            if acao == "CLICAR":
                if tab_random.revelar(l, c):
                    estado_r = "PERDEU"
                elif tab_random.verificar_vitoria():
                    estado_r = "VENCEU"
            elif acao == "TRAVOU":
                break

        pts_l = tab_logico.obter_pontuacao()
        pts_r = tab_random.obter_pontuacao()

        pontos_logico_total += pts_l
        pontos_random_total += pts_r

        if pts_l > pts_r:
            vitorias_logico += 1
        elif pts_r > pts_l:
            vitorias_random += 1
        else:
            empates += 1

        if (i + 1) % 1000 == 0:
            print(f"  -> Progresso: {i + 1} / {quantidade} jogos concluídos...")

    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio

    print("\n" + "="*50)
    print(f" RESULTADO FINAL DE {quantidade} PARTIDAS (Vence quem faz mais pontos)")
    print("="*50)
    print(f"Tempo de execução total: {tempo_total:.2f} segundos\n")

    print(f"--- IA LÓGICA ---")
    print(f"Vitórias em Combate: {vitorias_logico} ({(vitorias_logico/quantidade)*100:.2f}%)")
    print(f"Total de Pontos (Casas Seguras): {pontos_logico_total}")
    print(f"Média de Pontos por partida: {pontos_logico_total/quantidade:.2f}\n")

    print(f"--- IA ALEATÓRIA ---")
    print(f"Vitórias em Combate: {vitorias_random} ({(vitorias_random/quantidade)*100:.2f}%)")
    print(f"Total de Pontos (Casas Seguras): {pontos_random_total}")
    print(f"Média de Pontos por partida: {pontos_random_total/quantidade:.2f}\n")

    print(f"--- EMPATES ---")
    print(f"Quantidade: {empates} ({(empates/quantidade)*100:.2f}%)")
    print("="*50)

if __name__ == "__main__":
    rodar_simulacao(1000)
