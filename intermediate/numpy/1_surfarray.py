import pygame as pg
import numpy as np

# basic setup
pg.display.init()
screen = pg.display.set_mode((600,600))
pg.display.set_caption('surfarray')
running = True


# numpy stuff
surf = pg.Surface((128,128)) # surface with same size as the following array
array = np.zeros((128,128, 3), np.int32) # array with 3 dimensions, (for all R,G,B channels)


def array_values():
    global array
    # from 100 to 128, fills the elements on the array with a grey color
    array[100:128] = (100,100,100)
    # from -10 to 128
    array[-10:,:128] = (100,140,80)
    # from 0 to 100, fills with a red color
    array[:100] = (128,30,40)
    # from 0 to the end with step 10 draws "lines" for the x axis with a  green color
    array[:, ::10] = (0,100,30)
    for i in range(0,128,10):
        array[i] = (0,0,255)
    array[:,:1,:] = 0


def display_array():
    pg.surfarray.blit_array(surf, array)
    screen.blit(surf,(0,0))
    pg.display.flip()

screen.fill('white')

array_values()
display_array()

while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                running = False
            elif e.key == pg.K_SPACE:
                array_values()
                display_array()
            elif e.key == pg.K_r:
                array_values()
                array[:,:,1:] = 0
                display_array()
            elif e.key == pg.K_g:
                array_values()
                array[:, :, :1] = 0
                display_array()
            elif e.key == pg.K_b:
                array_values()
                array[:, :, :2] = 0
                display_array()
            elif e.key == pg.K_1:
                array_values()
                array = np.sort(array, axis=0)
                display_array()
            elif e.key == pg.K_2:
                #array_values()
                array[array == 255] = 100
                display_array()
