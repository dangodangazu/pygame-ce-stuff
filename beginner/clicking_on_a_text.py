# basic example of how to detect mouse clicks

import pygame 
from pygame.locals import MOUSEBUTTONDOWN, QUIT

pygame.init()
screen = pygame.display.set_mode((400,300)) #set your pygame window size
screen_rect = screen.get_rect() #get your window rectangle

font = pygame.font.Font(None, 50) # define your font
font_surf=font.render('CLICK ME!!', True, 'orange','black') #render the text you want to display

font_rect = font_surf.get_rect() #gets the font_surf rectangle, we need this so we can check clicks later
font_rect.center = screen_rect.center #sets the center of your font_surf, to the center of your pygame window

screen.fill('white') # fills the window in a white color

screen.blit(font_surf, font_rect) #blits your text on screen
pygame.display.flip() #updates the screen just once, in programs where you want things to move, call this inside your while loop instead

running = True
while running: 
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False
      print('Bye!')
      
    if event.type == MOUSEBUTTONDOWN: # this is the event we have to check for mouse clicks
      if font_rect.collidepoint(event.pos): # check if your mouse pos is inside of the area of your font_rect (i think)
        if event.button == 1: # check if left click was pressed (1 is left click, 2 is scroll button, 3 is right click)
          print('you clicked me ♥')
      else:
        print("you didn't click me :c")
