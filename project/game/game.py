# Importamos las bibliotecas

from multiprocessing.connection import wait
import os
import sys
import random
import pygame

from .config import *
from .platform import Platform
from .player import Player
from .wall import Wall
from .coin import Coin

# Defenimos una clase para el videojuego
class Game:

    # Definimos un metodo de inicializacion del videojuego
    def __init__(self):
        # Pintamos nuestra ventana
        pygame.init()
        # Generamos una ventana
        self.surface = pygame.display.set_mode((WIDTH,HEIGHT))
        # Titulo de la ventana
        pygame.display.set_caption(TITLE)
        # Conocer si la aplicacion se esta ejecutando o no
        self.running = True
        # 
        # self.playing = True
        # Actualizar los frames por segundo
        self.clock = pygame.time.Clock()
        # Colocamos una funete a nuestro score (Alcance)
        self.font = pygame.font.match_font(FONT)
        # Ruta absoluta de un archivo
        self.dir = os.path.dirname(__file__)
        # Ruta de la carpeta de sonidos
        self.dir_sounds = os.path.join(self.dir, 'sources/sounds')
        # Ruta de la carpeta de imagenes
        self.dir_images = os.path.join(self.dir, 'sources/sprites')


    # Definimos un metodo para iniciar el juego
    def start(self):
        # Damos un menu de opciones
        self.menu()
        # Ejecutar el metodo new
        self.new()

    # Definimos un metodo para crear un nuevo juego (Nueva partida)
    def new(self):
        # El scor comienza en 0
        self.score = 0
        # Nivel 0 del juego
        self.level = 0
        # 
        self.playing = True
        self.background =  pygame.image.load(os.path.join(self.dir_images, 'background.png'))
        # 
        self.generate_elements()
        # Ejecutar el metodo run
        self.run()

    # Crea los elementos deljuego
    def generate_elements(self):
        self.platform = Platform()
        self.player = Player(100, self.platform.rect.top - 200, self.dir_images)

        # Agregamos las paredes
        # self.wall = Wall(500, self.platform.rect.top)

        # Agrupar los diferentes sprites a utilizar en el video juego
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        # Agregamos la plataforma a la lista
        self.sprites.add(self.platform)
        self.sprites.add(self.player)
        # self.sprites.add(self.wall)

        self.generate_walls()
        # self.generate_coins()

    # Genera nuevos obstaculos
    def generate_walls(self):
        last_position = WIDTH + 400
        # Si no hay obstaculos entonces los generamos
        if not len(self.walls) > 0:
            for w in range(0, MAX_WALLS):
                # Posiciones aleatorias
                left = random.randrange( last_position + 800, last_position + 1600)
                # Generamos objetos de tipo wall
                wall = Wall(left, self.platform.rect.top, self.dir_images)
                last_position = wall.rect.right

                # Agrgar a las listas
                self.sprites.add(wall)
                self.walls.add(wall)
            
            # Cuando se genera un obstaculo se incrementa en 1 el nivel
            self.level += 1
            # Generamos mas monedas
            self.generate_coins()

    # 
    def generate_coins(self):
        last_position = WIDTH + 100

        for c in range(0, MAX_COINS):
            pos_x = random.randrange(last_position + 180, last_position + 300)

            # Colocamos todas las monedas a un altura de 100 pixeles
            coin = Coin(pos_x, 120, self.dir_images)

            last_position = coin.rect.right

            self.sprites.add(coin)
            self.coins.add(coin)

    # Definimos un metodo para correr el juego
    def run(self):
        # Iniciamos el ciclo del juego
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # Definimos un metodo para escuchar eventos
    def events(self):
        # Optenemos los objetos de eventos realizados
        for event in pygame.event.get():
            # Si cerramos la ventana detenemos la ejecucion del codigo
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit
                sys.exit()
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.player.jump()

        # Reiniciar el juego
        if key[pygame.K_r] and not self.playing:
            self.new()

    # Definimos un metodo para colocar los elementos en el juego
    def draw(self):
        # Colocar color a la superficie
        # self.surface.fill(BLACK)
        self.surface.blit(self.background, (0,0))
        # Pintamos el score en pantalla
        self.draw_text()
        # Dibujar todos los sprites que la lista almacene
        self.sprites.draw(self.surface)
        # Actualizamos la ventana
        pygame.display.flip()

    # Definimos un metodo para actualizar la pantalla
    def update(self):
        if not self.playing:
            return

        # Si hubo alguna colicion
        wall = self.player.collide_with(self.walls)
        if wall:
            if self.player.collide_bottom(wall):
                self.player.skid(wall)
            else:
                self.stop()

        # obsevamos los eventos de colicion
        coin = self.player.collide_with(self.coins)
        # Si existe una colicion
        if coin:
            self.score += 1
            # La moneda se destruye una vez se a colicionado con ella
            coin.kill()
            sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'coin.wav'))
            sound.play()

        # Actualizamos los sprites
        self.sprites.update()

        # validamos los desplazamientos con la plataforma
        self.player.validate_platform(self.platform)

        # Actualizamos lo elementos visibles y quitamos el resto
        self.update_elements(self.walls)
        self.update_elements(self.coins)

        # Generar obstaculos cuando no halla elementos en la lista walls
        self.generate_walls()

        # Damos un retardo a todas la animaciones
        pygame.time.delay(21)

    # Eliminamos Todos los elementos que no son visibles en pantalla para liberar memoria
    def update_elements(self, elements):
        for element in elements:
            # Si el elemento no es visible lo quitamos
            if not element. rect. right > 0:
                # Elimina el objeto
                element.kill()

    # Definimos un metodo para detener el video juego
    def stop(self):
        sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'lose.wav'))
        sound.play()
        # Detenemos al jugador
        self.player.stop()
        # Detenemos los objetos
        self.stop_elements(self.walls)

        self.playing = False

    # Detener todos los elementos
    def stop_elements(self, elements):
        for element in elements:
            element.stop()

    # Formato para el score
    def score_format(self):
        return 'Score : {}'.format(self.score)

    # Formato del nivel
    def level_format(self):
        return 'Level : {}'.format(self.level)

    # Pinta el score
    def draw_text(self):
        self.display_text(self.score_format(), 36, BLACK, WIDTH // 2, 30)
        self.display_text(self.level_format(), 36, BLACK, 80, TEXT_POSY)

        # Si el jugador ya no esta jugan 'Perdio'
        if not self.playing:
            self.display_text('Perdiste', 60, BLACK, WIDTH // 2, HEIGHT // 2)
            self.display_text('Preciona r para volver a comenzar', 30, BLACK, WIDTH // 2, 70)

    # Texto emn pantalla
    def display_text(self, text, size, color, pos_x, pos_y):
        # Obtenemos la fuente
        font = pygame.font.Font(self.font, size)
        # obtenemos el texto
        text = font.render(text, True, color)
        # Obtenemos el rectangulo
        rect = text.get_rect()
        # Posicion del texto
        rect.midtop = (pos_x, pos_y)
        # Pintamos el texto en pantalla
        self.surface.blit(text, rect)

    # Menu del juego
    def menu(self):
        self.surface.fill(GREEN_LIGHT)
        self.display_text('Presiona una tecla para comenzar', 36, BLACK, WIDTH // 2, 10)
        # Actualizamos la pantalla
        pygame.display.flip()
        # Esperamos un evento
        self.wait()

    # Metodo a la espera de eventos
    def wait(self):
        wait = True

        while wait:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYUP:
                    wait = False
