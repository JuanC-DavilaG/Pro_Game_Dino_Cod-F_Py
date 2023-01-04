import os
import pygame

from .config import *


class Player(pygame.sprite.Sprite):

    # Definimos el metodo init que se ereda de la clase padre
    def __init__(self, left, bottom, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.images = (
            pygame.image.load(os.path.join(dir_images, 'player1.png')),
            pygame.image.load(os.path.join(dir_images, 'jump.png')),
        )

        # self.image = pygame.Surface((40,40))
        # self.image = pygame.image.load(os.path.join(dir_images, 'player1.png'))
        self.image = self.images[0]
        # self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom

        self.pos_y = self.rect.bottom
        self.vel_y = 0

        self.can_jum = False

        self.playing = True

    # Metodo de colicion para el jugador y los obstaculos
    def collide_with(self, sprites):
        # Con quien coliciono
        objects = pygame.sprite.spritecollide(self, sprites, False)
        if objects:
            return objects[0]

    # Conocer si el jugador coliciono con la parte superior de un obstaculo
    def collide_bottom(self, wall):
        return self.rect.colliderect(wall.rect_top)

    # Sorfear sobre una pared
    def skid(self, wall):
        self.pos_y = wall.rect.top
        self.vel_y = 0
        self.can_jum = True
        # Cuando este sobre una pared volvemos a regresar a la imagen por defecto
        self.image = self.images[0]

    # Metodo de colicion para el jugador y la plataforma
    def validate_platform(self, platform):
        result = pygame.sprite.collide_rect(self, platform)
        if result:
            self.vel_y = 0
            self.pos_y = platform.rect.top
            self.can_jum = True
            # Cuando exista una colicion volvemos a regresar a la imagen por defecto
            self.image = self.images[0]

    def jump(self):
        if self.can_jum:
            self.vel_y = -24
            self.can_jum = False
            # Cuando el jugador salte cambiamos su imagen
            self.image = self.images[1]

    # Modelo fisico de aceleracion
    def update_pos(self):
        self.vel_y += PLAYER_GRAV
        self.pos_y += self.vel_y + 0.4 * PLAYER_GRAV

    # Actualizamos el valor de la posicion
    def update(self):
        if self.playing:
            self.update_pos()

            self.rect.bottom = self.pos_y

    # Detener el movimiento del jugador
    def stop(self):
        self.playing = False


