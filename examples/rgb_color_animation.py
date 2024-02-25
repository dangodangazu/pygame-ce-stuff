import pygame as pg
from math import sin

# basic setup
pg.init()
width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Sine Wave -> RGB color animation")
clock = pg.time.Clock()

t = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN:
            running = False

    # sine waves
    r = int(sin(t * 0.1 + 2 * t * 0.1) * 127 + 128)
    g = int(sin(t * 0.1 + 2 * t * 0.2) * 127 + 128)
    b = int(sin(t * 0.1 + 2 * t * 0.3) * 127 + 128)

    # Draw
    screen.fill('grey4')  # Clear the screen
    pg.draw.circle(screen, (r, g, b), (width // 2, height // 2), 200)
    pg.display.flip()

    # increment
    t += 0.1
    print(r,g,b)
    # Control the frame rate
    clock.tick(30)/1000
pg.quit()
