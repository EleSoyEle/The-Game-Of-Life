'''
=============================
|     The Game Of Life      |
=============================
'''
#Importamos librerias
from pygame.locals import *
import pygame as pg
import numpy as np
import sys
from utils import *
from multiprocessing import Pool

#Definimos el tamaño de la ventana en pixeles
screen_size = 500
#Definimos el tamaño que tendra cada celula en pixeles
cell_size = 10
#Colores en format RGB
colors = {
    'black':(0,0,0),
    'white':(255,255,255),
    'red':(255,0,0),
    'green':(0,255,0),
    'blue':(0,0,255)
}

#Definimos el numero de celulas con la siguente operacion {tamaño de pantalla / tamaño de cada celula}
num_cell = int(screen_size/cell_size)

def main():
    #Iniciamos la ventana del juego
    pg.init()
    #Pool para multiproceso
    pool = Pool(None)
    #Definimos pantalla
    screen = pg.display.set_mode((screen_size,screen_size))
    pg.display.set_caption("The Game Of Life")#Definimos el titulo
    screen.fill(colors['black'])#Definimos el color de la pantalla
    #Variables para facilitar el uso {pausa y si se borraran los estados}
    pause = True
    reset = False
    positions = np.random.randint(0,2,[num_cell,num_cell])#En esta variable estan todas las celulas
    while True:
        if reset:
            positions = np.zeros([num_cell,num_cell])
            reset = False
        detect(positions,cell_size)
        write_screen(screen,positions,num_cell,colors,cell_size)
        if not pause:
            #Actualizamos las posiciones
            positions = pool.map(multicell,[[positions,num_cell]])[0]
        #Leemos el teclado
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pause = not pause
                if event.key == K_c:
                    reset = True
        #Actualizamos la ventana
        pg.display.update()


if __name__ == '__main__':
    main()
