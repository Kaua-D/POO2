from simulacao import rodar_simulacao
from database import db, ResultadoSimulacao
from pony.orm import db_session
import time

class TestadorDeMapas:
    def __init__(self, quantidade=100):
        self.quantidade = quantidade

    @db_session
    def _salvar_resultado(self, tipo_mapa, linhas, colunas, num_bombas, resultados):
        ResultadoSimulacao(
            tipo_mapa=tipo_mapa,
            linhas=linhas,
            colunas=colunas,
            num_bombas=num_bombas,
            vitorias_logico=resultados["vitorias_logico"],
            vitorias_random=resultados["vitorias_random"],
            empates=resultados["empates"],
            pontos_logico=resultados["pontos_logico"],
            pontos_random=resultados["pontos_random"],
            quantidade_partidas=self.quantidade
        )

    def rodar(self):
        print("=== INICIANDO BATERIA DE TESTES AUTOMÁTICA ===")

        print("\n\n>>> INICIANDO TESTE: MAPA ESPAÇADO <<<")
        res_espacado = rodar_simulacao(self.quantidade, linhas=15, colunas=15, num_bombas=10)
        self._salvar_resultado("Espaçado", 15, 15, 10, res_espacado)

        print("\n\n>>> INICIANDO TESTE: MAPA MEDIANO <<<")
        res_mediano = rodar_simulacao(self.quantidade, linhas=15, colunas=15, num_bombas=38)
        self._salvar_resultado("Mediano", 15, 15, 38, res_mediano)

        print("\n\n>>> INICIANDO TESTE: MAPA DENSO <<<")
        res_denso = rodar_simulacao(self.quantidade, linhas=15, colunas=15, num_bombas=70)
        self._salvar_resultado("Denso", 15, 15, 70, res_denso)

        print("\n\n>>> INICIANDO TESTE: MAPA PEQUENO <<<")
        res_pequeno = rodar_simulacao(self.quantidade, linhas=10, colunas=10, num_bombas=15)
        self._salvar_resultado("Pequeno", 10, 10, 15, res_pequeno)

        print("\n\n>>> INICIANDO TESTE: MAPA GRANDE <<<")
        res_grande = rodar_simulacao(self.quantidade, linhas=20, colunas=20, num_bombas=80)
        self._salvar_resultado("Grande", 20, 20, 80, res_grande)

        print("\n=== BATERIA DE TESTES CONCLUÍDA E SALVA NO BANCO DE DADOS ===")

    def esperar(self, segundos=5):
        print(f"\nModo de espera ativado: Aguardando {segundos} segundos...")
        time.sleep(segundos)
        print("Modo de espera concluído.")

if __name__ == "__main__":
    testador = TestadorDeMapas(quantidade=100)
    testador.rodar()
    testador.esperar(2)
