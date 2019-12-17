# -*- coding: utf-8 -*-

#iMPORTACION DE MODULOS
import pygame
from pygame.locals import *
import sys
import time
import os
import random


#DECLARACION DE VARIABLES Y CONSTANTES
SCREEN_WIDTH= 1376
SCREEN_HEIGHT = 768
IMG_DIR = "imagenes" #variable para tener la dirección de la carpeta de imagenes
IMG_SON = "sonidos" #carpeta de audios 
font_name = pygame.font.match_font('arial')
BLACK= (0,0,0)

health_t= "salud"
score_t= "score"


#coordenadas del centro de la pantalla
x= SCREEN_WIDTH/2
y=SCREEN_HEIGHT/2


#CLASES Y FUNCIONES

def load_image(nombre, IMG_DIR, alpha=False): #FUNCION PARA ABRIR IMAGENES
    
    ruta=os.path.join(IMG_DIR, nombre) #se encuentra la ruta completa de la imagen
    try:
        image=pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: "+ ruta)
        sys.exit(1)
    #comprobar si la imagen tiene canal alpha (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image=image.convert()
    return image

def load_sound(nombre, IMG_SON): #FUNCION PARA APRIR AUDIO
    ruta= os.path.join(SON_DIR, nombre)
    try:
        sonido = pygame.mixer.Sound(ruta)
    except(pygame.error, message):
        print ("No se pudo cargar el sonido: ", ruta)
        sonido = None
    return Sonido



#Creacion de SPRITES / objetos en CLASES



class Dios(pygame.sprite.Sprite): #ES EL JUGADOR
    
    cambio_x=0
    cambio_y=0
    
    def __init__(self):     #PARAMETROS INICIALES DEL JUGADOR
        pygame.sprite.Sprite.__init__(self)
        self.image= load_image("dios.png", IMG_DIR, alpha=True)
        self.image=pygame.transform.scale(self.image, (100, 190))
        self.rect= self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2 #lo fja en el centro de x
        self.rect.centery = SCREEN_HEIGHT / 2 #lo fija en el centro de y
        #self.speed = [3, 3] #[0,1] : [x,y]
        self.health =100
        self.score=0
       
    
    def humano(self): #para que dios no se salga de los límites del mapa
        
        if self.rect.centerx> SCREEN_WIDTH:
            self.rect.centerx= 0 
        if self.rect.left< 0:
            self.rect.centerx= SCREEN_WIDTH
    
    def update(self): #cambios que se hacen en la pantalla
        self.gravedad()
        
        self.rect.centerx+= self.cambio_x
        self.rect.centery+= self.cambio_y
            
    def gravedad(self): #gravedad para que brinque
        if (self.cambio_y == 0):
            self.cambio_y = 1
        else:
            self.cambio_y += .35
        
        #si no se encuentra en el suelo
        if (self.rect.centery >= (SCREEN_HEIGHT/2) and self.cambio_y >= 0):
            self.cambio_y = 0
            self.rect.centery= (SCREEN_HEIGHT/2) 
    
    def saltar(self): #efecto de que brinque
        self.rect.centery+=2
        self.rect.centery-=2
        
        if self.rect.centery>= SCREEN_HEIGHT/2:
            self.cambio_y = -7
        
    def derecha(self): #movimiento a la derecha
        self.cambio_x = 10
    
    def izquierda(self): #movimiento a la izquierda
        self.cambio_x = -10
    
    def alto(self): #cuando ya no se mueve
        self.cambio_x = 0
        
        
         
class Mira(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= load_image("mirilla.png", IMG_DIR, alpha= True)
        self.image=pygame.transform.scale(self.image, (20, 20))
        self.rect= self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2 #lo fja en el centro de x
        self.rect.centery = SCREEN_HEIGHT / 2 #lo fija en el centro de y
        self.speed = [10, 10] #[0,1] : [x,y] 
    
    def humano(self):
        #para que la mirilla no se salga del mapa
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom= SCREEN_HEIGHT
        if self.rect.top<= 0:
            self.rect.top= 0   
            
class Rayo(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= load_image("rayo.png", IMG_DIR, alpha= True)
        self.image=pygame.transform.scale(self.image, (50, 50))
        self.rect= self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2 #lo fja en el centro de x
        self.rect.centery = SCREEN_HEIGHT / 2 #lo fija en el centro de y
        self.speed = [10, 10] #[0,1] : [x,y]        
        
        
class Enemigo1(pygame.sprite.Sprite): #SPRITE DEL TEC
    
    def __init__(self): #parametros iniciales
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("tec.png", IMG_DIR, alpha=True)
        self.image=pygame.transform.scale(self.image, (60,60))
        self.rect= self.image.get_rect()
        self.rect.centerx= random.randrange(0,1376)
        self.rect.centery= random.randrange(0,100)
    
       
    
    def cpu(self, dios): #lo que hace el cpu para que se mueva solo
        self.speed=[1,3] #velocidad en [x,y]
        if dios.rect.centerx <= SCREEN_WIDTH:
            if self.rect.centerx > dios.rect.centerx:
                self.rect.centerx -= self.speed[1]
            if self.rect.centerx < dios.rect.centerx:
                self.rect.centerx += self.speed[1]
            else:
                self.rect.centerx -= self.speed[1]            
        if self.rect.bottom >= 775:
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)
        self.rect.centery += 1
        
    def colision(self, objeto): #cuando choca con dios
        if self.rect.colliderect(objeto.rect):
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)
            objeto.health -=10
            
    
    def colision_rayo(self,objeto, dios): #cuando el rayo lo toca
        if self.rect.colliderect(objeto.rect):
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376) 
            dios.score+=10
        
        
class Enemigo2(pygame.sprite.Sprite): #sprite del examen reprobado
    
    def __init__(self): #parametros
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("exam.png", IMG_DIR, alpha=True)
        self.image=pygame.transform.scale(self.image, (60,60))
        self.rect= self.image.get_rect()
        self.rect.centerx= random.randrange(0,1376)
        self.rect.centery= random.randrange(0,100)       

    def cpu(self, dios): #la compu lo manipula
        self.speed=[0.25,3]
        if dios.rect.centerx <= SCREEN_WIDTH:
            if self.rect.centerx > dios.rect.centerx:
                self.rect.centerx -= self.speed[1]
            if self.rect.centerx < dios.rect.centerx:
                self.rect.centerx += self.speed[1]
            else:
                self.rect.centerx -= self.speed[1]   
        #si las coordenas= dios(x,y) entonces:                         
        if self.rect.centerx== dios.rect.centerx and self.rect.centery== dios.rect.centery:
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)            
        #si no choca con dios    
        elif self.rect.bottom >= 860:
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)
        self.rect.centery += 1
        
    def colision(self, dios): #si choca con dios
        if self.rect.colliderect(dios.rect):
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)
            dios.health-=10
    
    def colision_rayo(self,objeto,dios): #si el rayo lo toca
        if self.rect.colliderect(objeto.rect):
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)    
            dios.score+=10
        
class Enemigo3(pygame.sprite.Sprite): #sprite del enemigo Yellow Devil
    def __init__(self): #parametros iniciales
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("devil.png", IMG_DIR, alpha=True)
        self.image=pygame.transform.scale(self.image, (60,60))
        self.rect= self.image.get_rect()
        self.rect.centerx= random.randrange(0,1376)
        self.rect.centery= random.randrange(0,100)       

    def cpu(self, dios): #lo que hace que se mueva solo
        self.speed=[0.25,3]
        if dios.rect.centerx <= SCREEN_WIDTH:
            if self.rect.centerx > dios.rect.centerx:
                self.rect.centerx -= self.speed[1]
            if self.rect.centerx < dios.rect.centerx:
                self.rect.centerx += self.speed[1]
            else:
                self.rect.centerx -= self.speed[1]   
        #si las coordenas= dios(x,y) entonces:                         
        if self.rect.centerx== dios.rect.centerx and self.rect.centery== dios.rect.centery:
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)            
        #si no choca con dios    
        elif self.rect.bottom >= 1200:
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)
        self.rect.centery += 1    
    
    def colision(self, dios): #si choca con Dios
        if self.rect.colliderect(dios.rect):
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)
            dios.health-=10
    
    def colision_rayo(self,objeto,dios): #si el rayo lo toca
        if self.rect.colliderect(objeto.rect):
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)    
            dios.score+=10
            
        
        
class Salud(pygame.sprite.Sprite): #spite del ilumminati que da salud
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("ilumi.png", IMG_DIR, alpha=True)
        self.image=pygame.transform.scale(self.image, (60,60))
        self.rect= self.image.get_rect()
        self.rect.centerx= random.randrange(0,1376)
        
    def cpu(self): #hace que se caiga
        self.speed=[0,0.2]
        self.rect.centery +=3
        if self.rect.bottom>= 3000:
            self.rect.centery= random.randrange(-40,-10)
            self.rect.centerx = random.randrange(0,1376)
            
    def colision(self, dios): #hace que vuelva a caer si dios lo toca
        if self.rect.colliderect(dios.rect):
            self.rect.centery = random.randrange(-10,0)
            self.rect.centerx = random.randrange(0,1376)
            dios.health+=30
        
        
def menu(): #LA PANTALLA QUE INICIA EL JUEGO
    screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Ajusta el tamaño de la ventana emergente
    image = load_image("inicio.jpg", IMG_DIR, alpha=True)
    image=pygame.transform.scale(image, (1376,768))    
    screen.blit(image, (0,0))
    pygame.display.flip()    
    
#MAIN


def draw_text(surf, text, size, x, y): #DEPLIEGA EL TEXTO
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def main(): #LO QUE CORRE TODO
    pygame.init()
    file = 'music_01.mp3' #CANCION DE FONDO
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()    
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        
    screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Ajusta el tamaño de la ventana emergente
    pygame.display.set_caption("Rayo Emprendedor #ForTheWin")
    
    pygame.mixer.music.load('music_01.mp3')
    pygame.mixer.music.play(-1)
    
    
    
    while True:
        for event in pygame.event.get():
            if event.type != pygame.KEYDOWN: #MIENTAS NO SE PRESIONE UNA TECLA, SEGUIRÁ MOSTRANDO LA PANTALLA INICIAL
                menu()
    
            else:
                #fondo y objetoo
                fondo=load_image("fondo.jpg", IMG_DIR, alpha=False)
                screen.blit(fondo, (0,0))
                #se crean los objetos
                dios=Dios()
                mira=Mira()
                rayo=Rayo()
                enemy=Enemigo1()
                enemy1=Enemigo2()
                enemy2=Enemigo3()
                salud=Salud()
                clock=pygame.time.Clock() 
                pygame.key.set_repeat(1,25) #activa la repetición del TECLADO
                pygame.mouse.set_visible(False) #escondemos el mouse de la pantalla
                
                
                
                #blucle del juego SIEMPRE AL FINAL
                while dios.health >0: #mientras la salud de Dios sea mayo a 0 se va a seguir jugando, una vez que no se cumpla VUELVE A EMPEZAR
                    clock.tick(60) #FPS
                    pos_mouse= pygame.mouse.get_pos()
                    mov_mouse= pygame.mouse.get_rel() # desplazamieto del mouse
                    
                    #actualizar objetos en pantalla
                    dios.humano()
                    mira.humano()
                    salud.cpu()
                    enemy.cpu(dios)
                    enemy1.cpu(dios)
                    enemy2.cpu(dios)
                    keys=pygame.key.get_pressed()
                    
                    #comprobacion de colisiones
                    enemy.colision(dios)
                    enemy.colision_rayo(rayo, dios)
                    enemy1.colision(dios)
                    enemy1.colision_rayo(rayo,dios)
                    enemy2.colision(dios)
                    enemy2.colision_rayo(rayo,dios)
                    salud.colision(dios)
                    
                    if (dios.health>= 100):
                        dios.health=100 #si toma muchos iluminatis se mantiene en 100 como maximo

                    if (dios.health<=0): #una vez que tiene 0 de salud lo manda al inicio, la pantalla inicial
                        menu()
                        break
                        
                    
                    #entradas del teclado y mouse
                    for event in pygame.event.get(): #ciclo que siempre se pregunta si se da QUIT
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if mov_mouse[0] != 0 and mov_mouse[1] != 0: #si el mouse se mueve en X y Y
                            mira.rect.centerx = pos_mouse[0]
                            mira.rect.centery = pos_mouse[1]
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                objetivo= pygame.mouse.get_pos()
                                rayo.rect.centerx = pos_mouse[0]
                                rayo.rect.centery = pos_mouse[1]      
                                
                        if event.type == pygame.KEYDOWN: #si una tecla se presiona...
                            if keys[K_a]: 
                                #dios.rect.centerx -= 10 
                                dios.izquierda()
                            if keys[K_d]: 
                                #dios.rect.centerx += 10 
                                dios.derecha()
                            if keys[K_w]:
                                dios.saltar()
                            if keys[K_ESCAPE]:
                                sys.exit()
                        
                        if event.type == pygame.KEYUP: #si una tecla deja de presionarse
                            if keys[K_a]:
                                dios.alto()
                            if keys[K_d]:
                                dios.alto() 
                                
                                
                    dios.update()
                    
                    #actualizamos la pantalla
                    screen.blit(fondo,(0,0))
                    fondo=pygame.transform.scale(fondo, (1376, 768))
                    screen.blit(dios.image, dios.rect)
                    screen.blit(mira.image, mira.rect)
                    screen.blit(rayo.image, rayo.rect)
                    screen.blit(enemy.image, enemy.rect)
                    screen.blit(enemy1.image, enemy1.rect)
                    screen.blit(enemy2.image, enemy2.rect)
                    screen.blit(salud.image, salud.rect)
                    draw_text(screen, health_t, 40, 686, 700) #coordenadas de "salud"
                    draw_text(screen, str(dios.health), 30, 686, 730)
                    draw_text(screen, score_t, 40, 200,700) #coordenadas del "score"
                    draw_text(screen, str(dios.score), 30, 300, 710)
                    pygame.display.flip()
            

main() #INICIA EL PROGRAMA





