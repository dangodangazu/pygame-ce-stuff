import pygame
from pygame.locals import *

pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

#font = pygame.font.Font('path_of_your_font', 36) # you can pass None instead of a path, if you don't have a font
font = pygame.font.SysFont('Console',36) # or use a SysFont instead (Arial, Times New Roman, Century, Console, etc)

text = font.render('Hello World', True, 'red') #rendering the text we want

# setting a transparency, the lower the value is the more transparent, max value you can pass is 255, but 255 just means
# it does not have transparency at all, modifying this value too low, sometimes make fonts look weird  
text.set_alpha(255)

# the usual while loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # filling the screen in a black color
    screen.fill('black')
    if event.type == pygame.MOUSEMOTION:
        screen.blit(text, event.pos)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2)) #blitting the text on the center of the screen
    screen.blit(text, (width // 2 - text.get_width() // 2+2, height // 2 - text.get_height() // 2+2)) #blitting again in almost the same position to get a "3d effect"
    pygame.display.flip()

# exiting pygame when you exit the while loop
pygame.quit()
