import pygame
import constants

class Celula:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.tem_bomba = False
        self.revelada = False
        self.marcada = False
        self.vizinhos_com_bomba = 0

    def desenhar(self, tela, offset_x=0):
        x = (self.coluna * constants.TAMANHO_CELULA) + offset_x
        y = (self.linha * constants.TAMANHO_CELULA) + constants.ALTURA_MENU
        rect = pygame.Rect(x, y, constants.TAMANHO_CELULA, constants.TAMANHO_CELULA)

        if not self.revelada:
            pygame.draw.rect(tela, constants.COR_OCULTA, rect)
            if self.marcada:
                texto = constants.FONTE_NUMEROS.render("F", True, constants.COR_BOMBA)
                tela.blit(texto, (x + 12, y + 5))
        else:
            pygame.draw.rect(tela, constants.COR_REVELADA, rect)
            if self.tem_bomba:
                pygame.draw.circle(tela, constants.COR_TEXTO, (x + constants.TAMANHO_CELULA//2, y + constants.TAMANHO_CELULA//2), 10)
            elif self.vizinhos_com_bomba > 0:
                texto = constants.FONTE_NUMEROS.render(str(self.vizinhos_com_bomba), True, constants.COR_TEXTO)
                tela.blit(texto, (x + 12, y + 5))
        
        pygame.draw.rect(tela, constants.COR_LINHA, rect, 1)