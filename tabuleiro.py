import random
from celula import Celula
import constants

class Tabuleiro:
    def __init__(self, gerar_bombas=True):
        self.matriz = [[Celula(l, c) for c in range(constants.COLUNAS)] for l in range(constants.LINHAS)]
        if gerar_bombas:
            self.gerar_bombas()
            self.calcular_vizinhos()

    def gerar_bombas(self):
        bombas_plantadas = 0
        while bombas_plantadas < constants.NUM_BOMBAS:
            l = random.randint(0, constants.LINHAS - 1)
            c = random.randint(0, constants.COLUNAS - 1)
            if not self.matriz[l][c].tem_bomba:
                self.matriz[l][c].tem_bomba = True
                bombas_plantadas += 1

    def calcular_vizinhos(self):
        para_verificar = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for l in range(constants.LINHAS):
            for c in range(constants.COLUNAS):
                celula = self.matriz[l][c]
                if celula.tem_bomba: continue
                contagem = 0
                for dl, dc in para_verificar:
                    nl, nc = l + dl, c + dc
                    if 0 <= nl < constants.LINHAS and 0 <= nc < constants.COLUNAS:
                        if self.matriz[nl][nc].tem_bomba:
                            contagem += 1
                celula.vizinhos_com_bomba = contagem

    def clonar_de(self, outro_tabuleiro):
        for l in range(constants.LINHAS):
            for c in range(constants.COLUNAS):
                self.matriz[l][c].tem_bomba = outro_tabuleiro.matriz[l][c].tem_bomba
        self.calcular_vizinhos()

    def revelar(self, linha, coluna):
        celula = self.matriz[linha][coluna]
        if celula.revelada or celula.marcada:
            return False

        celula.revelada = True

        if celula.tem_bomba:
            return True

        if celula.vizinhos_com_bomba == 0:
            para_verificar = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            for dl, dc in para_verificar:
                nl, nc = linha + dl, coluna + dc
                if 0 <= nl < constants.LINHAS and 0 <= nc < constants.COLUNAS:
                    self.revelar(nl, nc)
        
        return False

    def verificar_vitoria(self):
        celulas_reveladas = 0
        for linha in self.matriz:
            for celula in linha:
                if celula.revelada and not celula.tem_bomba:
                    celulas_reveladas += 1
        
        total_celulas_seguras = (constants.LINHAS * constants.COLUNAS) - constants.NUM_BOMBAS
        return celulas_reveladas == total_celulas_seguras

    def obter_pontuacao(self):
        pontos = 0
        for linha in self.matriz:
            for celula in linha:
                if celula.revelada and not celula.tem_bomba:
                    pontos += 1
        return pontos

    def revelar_todas_bombas(self):
        for l in self.matriz:
            for c in l:
                if c.tem_bomba:
                    c.revelada = True

    def desenhar(self, tela, offset_x=0):
        for linha in self.matriz:
            for celula in linha:
                celula.desenhar(tela, offset_x)