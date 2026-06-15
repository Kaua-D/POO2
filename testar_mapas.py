from simulacao import rodar_simulacao

def testar_todos_os_mapas():
    quantidade = 100

    # 1. Espaçado: 15x15, 10 bombas
    print("\n\n>>> INICIANDO TESTE: MAPA ESPAÇADO <<<")
    rodar_simulacao(quantidade, linhas=15, colunas=15, num_bombas=10)

    # 2. Mediano: 15x15, 38 bombas
    print("\n\n>>> INICIANDO TESTE: MAPA MEDIANO <<<")
    rodar_simulacao(quantidade, linhas=15, colunas=15, num_bombas=38)

    # 3. Denso: 15x15, 70 bombas
    print("\n\n>>> INICIANDO TESTE: MAPA DENSO <<<")
    rodar_simulacao(quantidade, linhas=15, colunas=15, num_bombas=70)

    # 4. Pequeno (Novo): 10x10, 15 bombas
    print("\n\n>>> INICIANDO TESTE: MAPA PEQUENO <<<")
    rodar_simulacao(quantidade, linhas=10, colunas=10, num_bombas=15)

    # 5. Grande (Novo): 20x20, 80 bombas
    print("\n\n>>> INICIANDO TESTE: MAPA GRANDE <<<")
    rodar_simulacao(quantidade, linhas=20, colunas=20, num_bombas=80)

if __name__ == "__main__":
    testar_todos_os_mapas()
