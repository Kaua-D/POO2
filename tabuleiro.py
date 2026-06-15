import random
from celula import Celula
import constants

class Tabuleiro:
    def __init__(self, linhas, colunas, num_bombas, gerar_bombas=True):
        self.linhas = linhas
        self.colunas = colunas
        self.num_bombas = num_bombas
        self.matriz = [[Celula(l, c) for c in range(self.colunas)] for l in range(self.linhas)]
        if gerar_bombas:
            self.gerar_bombas()
            self.calcular_vizinhos()

    def gerar_bombas(self):
        bombas_plantadas = 0
        while bombas_plantadas < self.num_bombas:
            l = random.randint(0, self.linhas - 1)
            c = random.randint(0, self.colunas - 1)
            if not self.matriz[l][c].tem_bomba:
                self.matriz[l][c].tem_bomba = True
                bombas_plantadas += 1

    def calcular_vizinhos(self):
        para_verificar = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for l in range(self.linhas):
            for c in range(self.colunas):
                celula = self.matriz[l][c]
                if celula.tem_bomba: continue
                contagem = 0
                for dl, dc in para_verificar:
                    nl, nc = l + dl, c + dc
                    if 0 <= nl < self.linhas and 0 <= nc < self.colunas:
                        if self.matriz[nl][nc].tem_bomba:
                            contagem += 1
                celula.vizinhos_com_bomba = contagem

    def clonar_de(self, outro_tabuleiro):
        for l in range(self.linhas):
            for c in range(self.colunas):
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
                if 0 <= nl < self.linhas and 0 <= nc < self.colunas:
                    self.revelar(nl, nc)

        return False

    def verificar_vitoria(self):
        celulas_reveladas = 0
        for linha in self.matriz:
            for celula in linha:
                if celula.revelada and not celula.tem_bomba:
                    celulas_reveladas += 1

        total_celulas_seguras = (self.linhas * self.colunas) - self.num_bombas
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

    def desenhar(self, tela, offset_x=0, offset_y=None):
        for linha in self.matriz:
            for celula in linha:
                celula.desenhar(tela, offset_x, offset_y)
