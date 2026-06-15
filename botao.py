import pygame
import constants

class Botao:
    def __init__(self, x, y, largura, altura, texto):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto

    def desenhar(self, tela):
        pos_mouse = pygame.mouse.get_pos()
        cor = constants.COR_BOTAO_HOVER if self.rect.collidepoint(pos_mouse) else constants.COR_BOTAO
        pygame.draw.rect(tela, cor, self.rect, border_radius=5)
        pygame.draw.rect(tela, constants.COR_TEXTO, self.rect, 2, border_radius=5)
        
        texto_render = constants.FONTE_BOTAO.render(self.texto, True, constants.COR_TEXTO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        tela.blit(texto_render, texto_rect)

    def foi_clicado(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)