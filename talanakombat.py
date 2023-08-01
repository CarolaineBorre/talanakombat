import sys
import pygame

ANCHO = 1000
ALTO = 600
FPS = 60
VELOCIDAD = 10
GRAVEDAD = 7
BLANCO = (255,255,255)
NEGRO = (0,0,0)
ROJO = (255,0,0)
AZUL = (0,0,255)
VERDE = (0,255,0)
AMARILLO = (255,255,0)
VENTANA = pygame.display.set_mode((ANCHO,ALTO))

JUGADOR_1_TAMAÑO = 150
JUGADOR_1_ESCALE = 4
JUGADOR_1_OFFSET = [350, 400]
JUGADOR_1_DATOS = [JUGADOR_1_TAMAÑO,JUGADOR_1_ESCALE,JUGADOR_1_OFFSET]
JUGADOR_2_TAMAÑO = 200
JUGADOR_2_ESCALE = 3
JUGADOR_2_OFFSET = [250, 550]
JUGADOR_2_DATOS = [JUGADOR_2_TAMAÑO,JUGADOR_2_ESCALE,JUGADOR_2_OFFSET]

#cargar imagenes
BACKGROUND = pygame.image.load("assets/imagenes/background/background.jpg")
HOJA_PLAYER_1 = pygame.image.load("assets/imagenes/Huntress/Sprites/Attack.png")
HOJA_PLAYER_2 = pygame.image.load("assets/imagenes/Martial Hero/Sprites/Attack.png")

#numero de pasos de la animacion
PASOS_PLAYER_1 = [5,5,7,8,2,8,2,8,3]
PASOS_PLAYER_2 = [6,6,6,2,8,2,8,4,4]

class Kombat:
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        pygame.display.set_caption("KOMBAT")
        clock = pygame.time.Clock()

        #Tonyn Stallone
        jugador_1 = pygame.sprite.Group()
        player_1 = Jugador(1,300,500,False,JUGADOR_1_DATOS,HOJA_PLAYER_1,PASOS_PLAYER_1)
        jugador_1.add(player_1)

        #Arnaldor Shuatseneguer
        jugador_2 = pygame.sprite.Group()
        player_2 = Jugador(2,700,500,True,JUGADOR_2_DATOS,HOJA_PLAYER_2,PASOS_PLAYER_2)
        jugador_2.add(player_2)

        jugando = True
        while jugando:
            clock.tick(FPS)
            self.pintar()
            self.barra(player_1.salud ,20,20)
            self.barra(player_2.salud,580,20)

            jugador_1.update(player_2)
            # jugador_2.update(player_1)

            jugador_1.draw(VENTANA)
            jugador_2.draw(VENTANA)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False

            pygame.display.flip()

        pygame.quit()

    def pintar(self):
        #pinta el background
        TAMAÑO = pygame.transform.scale(BACKGROUND, (ANCHO, ALTO))
        VENTANA.blit(TAMAÑO,(0,0))
    
    def barra(self,salud,x,y):
        #salud de los jugadores
        ratio = salud / 6
        #pinta barra de salud
        pygame.draw.rect(VENTANA,BLANCO,(x - 1 ,y - 2 ,404,34))
        pygame.draw.rect(VENTANA,ROJO,(x,y,400,30))
        pygame.draw.rect(VENTANA,AMARILLO,(x,y,400 * ratio,30))
    
class Jugador(pygame.sprite.Sprite):
    def __init__(self,player,x,y,flip,data,sprite_sheet,animation_steps):
        super().__init__()
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        
        self.animation_list = self.cargar_imagenes(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x,y,self.offset[0],self.offset[1]))
        # img = pygame.transform.flip(self.image, self.flip, False)
        self.rect.center = (x, y)
        #variable saltar
        self.saltar = False
        self.atacar = False
        self.tipo_ataque = 0
        self.salud = 6
        # VENTANA.blit(self.image, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
       
        # self.image = pygame.Surface((80,180))
        # self.image.fill(VERDE)
        # self.rect = pygame.Rect((x,y,80,180))
        # img = pygame.transform.flip(self.image, self.flip, False)
        # VENTANA.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        # self.rect.center = (x, y)

        #velocidad inicial (quieto)
        self.velocidad_x = 0
        self.velocidad_y = 0


    def cargar_imagenes(self,sprite_sheet,animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size , self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    
    # def draw(self):
    #     #ubicacion nuevo personaje
    #     pygame.draw.rect(VENTANA, VERDE, self.rect)
    #     VENTANA.blit(self.image, (self.rect.x, self.rect.y))
        
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        VENTANA.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def update(self,enemigo):
        #velocidad predeterminada
        self.velocidad_x = 0
        self.velocidad_y = 0
        
        #mantiene las techas pulsadas
        teclas = pygame.key.get_pressed()
        #solo puede realizar una accion mientras no haya atacado
        if self.atacar == False:
            #   MOVIMIENTOS #
            #mueve a la izquierda
            if teclas[pygame.K_a]:
                self.velocidad_x = -VELOCIDAD

            #mueve a la derecha
            if teclas[pygame.K_d]:
                self.velocidad_x = VELOCIDAD
            
            #ataca (golpea)
            if teclas[pygame.K_p] or teclas[pygame.K_k]  and self.atacar == False:
                self.ataque(enemigo)
                
                #determina el tipo de ataque 
                if teclas[pygame.K_p]:
                    self.tipo_ataque = 1
                if teclas[pygame.K_k]:
                    self.tipo_ataque = 2

            #salto
            if teclas[pygame.K_w] and self.saltar == False:
                self.velocidad_y = -30
                # self.saltar = True

        #aplicar gravedad
        self.velocidad_y += GRAVEDAD    
        self.rect.y += self.velocidad_y
        
        #actualiza la posicion del personaje
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        #limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0

        #limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

        #limita el margen arriba
        if self.rect.top < 0:
            self.rect.top = 0

        #limita el margen abajo
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

        #Limita el margen con enemigo
        if enemigo.rect.centerx > self.rect.centerx:
            self.limite = False
        else:
            self.rect.x -= 60
            self.limite = True

    def ataque(self,enemigo):
        self.atacar = True
        ataque_rect = pygame.Rect(self.rect.centerx+40 - (2 * self.rect.width * self.limite), self.rect.y,2 * self.rect.width, self.rect.height)
        if ataque_rect.colliderect(enemigo):
            enemigo.salud -= 1
            print("golpe")

        pygame.draw.rect(VENTANA,ROJO,ataque_rect)
    
    
        

Kombat()