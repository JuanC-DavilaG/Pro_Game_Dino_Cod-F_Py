import pygame

from .config import *

class Platform(pygame.sprite.Sprite):   # La clase hereda de pygame

    # LLamamos al metodo init
    def __init__(self):

        # Ejecutamos el metodo init de la clase padre
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(((WIDTH, HEIGHT)))
        self.image.fill(GREEN)

        # Obligatorio para usar el metodo Sprite definir una posiscion en 'x' y en 'y'
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 40