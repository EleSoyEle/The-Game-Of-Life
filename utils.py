from numpy.core.einsumfunc import _parse_possible_contraction
import pygame as pg
import numpy as np

#Creamos la funcion que dibujara la celula viva o muerta
def write_cube(screen,is_cell,matrix_x,matrix_y,colors,cell_size):
    pg.draw.rect(screen,colors['white'] if is_cell else colors['black'],[matrix_x*cell_size,matrix_y*cell_size,cell_size,cell_size])

#Creamos la funcion que dibujara todas las celulas
def multiwrite(args):
    write_screen(*args)

def write_screen(screen,positions,num_cell,colors,cell_size):
    for x in range(num_cell):
        for y in range(num_cell):
            write_cube(screen,True if positions[x][y] == 1 else False,x,y,colors,cell_size)


#Funcion que detectara el mouse y modificara los estados de las celulas
def detect(positions,cell_size):
    pos = pg.mouse.get_pos()
    if pg.mouse.get_pressed()[0] == 1:
        positions[int(pos[0]/cell_size)][int(pos[1]/cell_size)] = 1
    elif pg.mouse.get_pressed()[2] == 1:
        positions[int(pos[0]/cell_size)][int(pos[1]/cell_size)] = 0

def get_lateral_states(cp_pos,x,y,num_cell):
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
    return lateral_states

#La funcion mas importante, aqui se aplican todas las reglas del juego, tambien se detectan los estados etc...
def multicell(args):
    return evaluate_cells(args[0],args[1])

def evaluate_cells(positions,num_cell):
    cp_pos = np.copy(positions)
    new_pos = np.copy(positions)
    for x in range(num_cell):
        for y in range(num_cell):
            lateral_states = get_lateral_states(cp_pos,x,y,num_cell)
            num = 0
            for state in lateral_states:
                if state == 1:
                    num += 1
            if num == 2:
                new_pos[x][y] = 1 if positions[x][y] == 1 else 0
            if num == 3:
                new_pos[x][y] = 1
            elif num <= 1 or num >= 4:
                new_pos[x][y] = 0
    return new_pos