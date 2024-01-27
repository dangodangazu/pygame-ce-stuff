import pygame

pygame.init() # this initialize all the stuff you will need
screen = pygame.display.set_mode((400,300)) # create your pygame window, (400 width, 300 height)

pygame.display.set_caption('Opening a pygame window') # give your program a title

running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: # This, constantly checks if you click on [x] (topright of your pygame window)
      pygame.quit()               # if you did, quits pygame, and running will be False.
      running = False             # This enables the user to close the window.