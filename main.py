import pygame
from jogo import Jogo

def main():
    pygame.init()
    meu_jogo = Jogo()
    meu_jogo.rodar()
    pygame.quit()

if __name__ == "__main__":
    main()