import random
import constants

class JogadorLogico:
    def __init__(self, tabuleiro):
        self.tabuleiro = tabuleiro

    def obter_vizinhos(self, linha, coluna):
        vizinhos = []
        para_verificar = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for dl, dc in para_verificar:
            nl, nc = linha + dl, coluna + dc
            if 0 <= nl < constants.LINHAS and 0 <= nc < constants.COLUNAS:
                vizinhos.append(self.tabuleiro.matriz[nl][nc])
        return vizinhos

    def realizar_jogada(self):
        celulas_reveladas = sum(1 for l in self.tabuleiro.matriz for c in l if c.revelada)
        if celulas_reveladas == 0:
            return ("CLICAR", constants.LINHAS // 2, constants.COLUNAS // 2)

        fez_algo = False
        
        for l in range(constants.LINHAS):
            for c in range(constants.COLUNAS):
                celula = self.tabuleiro.matriz[l][c]
                if celula.revelada and not celula.tem_bomba and celula.vizinhos_com_bomba > 0:
                    vizinhos = self.obter_vizinhos(l, c)
                    ocultos = [v for v in vizinhos if not v.revelada and not v.marcada]
                    marcados = [v for v in vizinhos if v.marcada]

                    if len(ocultos) > 0 and celula.vizinhos_com_bomba == len(ocultos) + len(marcados):
                        for oc in ocultos:
                            oc.marcada = True
                            fez_algo = True

        for l in range(constants.LINHAS):
            for c in range(constants.COLUNAS):
                celula = self.tabuleiro.matriz[l][c]
                if celula.revelada and not celula.tem_bomba and celula.vizinhos_com_bomba > 0:
                    vizinhos = self.obter_vizinhos(l, c)
                    ocultos = [v for v in vizinhos if not v.revelada and not v.marcada]
                    marcados = [v for v in vizinhos if v.marcada]

                    if len(ocultos) > 0 and celula.vizinhos_com_bomba == len(marcados):
                        return ("CLICAR", ocultos[0].linha, ocultos[0].coluna)

        if fez_algo:
            return ("MARCOU", -1, -1)

        opcoes = [(l, c) for l in range(constants.LINHAS) for c in range(constants.COLUNAS) if not self.tabuleiro.matriz[l][c].revelada and not self.tabuleiro.matriz[l][c].marcada]
        if opcoes:
            l, c = random.choice(opcoes)
            return ("CLICAR", l, c)
        return ("TRAVOU", -1, -1)

class JogadorAleatorio:
    def __init__(self, tabuleiro):
        self.tabuleiro = tabuleiro

    def realizar_jogada(self):
        opcoes = []
        for l in range(constants.LINHAS):
            for c in range(constants.COLUNAS):
                celula = self.tabuleiro.matriz[l][c]
                if not celula.revelada and not celula.marcada:
                    opcoes.append((l, c))
        
        if opcoes:
            l, c = random.choice(opcoes)
            return ("CLICAR", l, c)
        return ("TRAVOU", -1, -1)