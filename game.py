'''
=============================
|     The Game Of Life      |
=============================
'''
#Importamos librerias
from pygame.locals import *
import pygame as pg
import numpy as np
import time
import sys


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

#Creamos la funcion que dibujara la celula viva o muerta
def write_cube(screen,is_cell,matrix_x,matrix_y):
    pg.draw.rect(screen,colors['white'] if is_cell else colors['black'],[matrix_x*cell_size,matrix_y*cell_size,cell_size,cell_size])

#Creamos la funcion que dibujara todas las celulas
def write_screen(screen,positions):
    for x in range(num_cell):
        for y in range(num_cell):
            write_cube(screen,True if positions[x][y] == 1 else False,x,y)

#Funcion que detectara el mouse y modificara los estados de las celulas
def detect(positions):
    pos = pg.mouse.get_pos()
    if pg.mouse.get_pressed()[0] == 1:
        positions[int(pos[0]/cell_size)][int(pos[1]/cell_size)] = 1
    elif pg.mouse.get_pressed()[2] == 1:
        positions[int(pos[0]/cell_size)][int(pos[1]/cell_size)] = 0


#La funcion mas importante, aqui se aplican todas las reglas del juego, tambien se detectan los estados etc...
def evaluate_cells(positions):
    cp_pos = np.copy(positions)
    for x in range(num_cell):
        for y in range(num_cell):
            lateral_states = [
                cp_pos[x-1 if x > 0 else num_cell-1][y],
                cp_pos[x+1 if x < num_cell-1 else 0][y],
                cp_pos[x][y-1 if y > 0 else num_cell-1],
                cp_pos[x][y+1 if y < num_cell-1 else 0],
                cp_pos[x-1 if x > 0 else num_cell-1][y-1 if y > 0 else num_cell-1],
                cp_pos[x-1 if x > 0 else num_cell-1][y+1 if y < num_cell-1 else 0],
                cp_pos[x+1 if x < num_cell-1 else 0][y-1 if y > 0 else num_cell-1],
                cp_pos[x+1 if x < num_cell-1 else 0][y+1 if y < num_cell-1 else 0],
                ]
            num = 0
            for state in lateral_states:
                if state == 1:
                    num += 1
            if num == 2:
                positions[x][y] = 1 if positions[x][y] == 1 else 0
            if num == 3:
                positions[x][y] = 1
            elif num <= 1 or num >= 4:
                positions[x][y] = 0


def main():
    #Iniciamos la ventana del juego
    pg.init()
    screen = pg.display.set_mode((screen_size,screen_size))
    
    pg.display.set_caption("The Game Of Life")#Definimos el titulo
    screen.fill(colors['black'])#Definimos el color de la pantalla
    #Variables para facilitar el uso {pausa y si se borraran los estados}
    pause = True
    reset = False
    positions = np.zeros([num_cell,num_cell])#En esta variable estan todas las celulas
    while True:
        if reset:
            positions = np.zeros([num_cell,num_cell])
            reset = False
        detect(positions)
        write_screen(screen,positions)
        if not pause:
            evaluate_cells(positions)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pause = not pause
                if event.key == K_c:
                    reset = True

        pg.display.update()


if __name__ == '__main__':
    main()
