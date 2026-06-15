import pygame

pygame.font.init()

TAMANHO_CELULA = 30
ESPACO_MEIO = 40
ALTURA_MENU = 140

COR_FUNDO = (192, 192, 192)
COR_OCULTA = (150, 150, 150)
COR_REVELADA = (200, 200, 200)
COR_LINHA = (100, 100, 100)
COR_TEXTO = (0, 0, 0)
COR_BOMBA = (255, 0, 0)
COR_BOTAO = (100, 200, 100)
COR_BOTAO_HOVER = (120, 220, 120)

COR_LOGICO = (10, 100, 200)
COR_RANDOM = (200, 100, 10)
COR_VITORIA = (46, 204, 113)

FONTE_NUMEROS = pygame.font.SysFont('Arial', 24, bold=True)
FONTE_BOTAO = pygame.font.SysFont('Arial', 18, bold=True)
FONTE_PLACARES = pygame.font.SysFont('Arial', 20, bold=True)
FONTE_TITULOS = pygame.font.SysFont('Arial', 22, bold=True)
FONTE_VENCEDOR = pygame.font.SysFont('Arial', 26, bold=True)