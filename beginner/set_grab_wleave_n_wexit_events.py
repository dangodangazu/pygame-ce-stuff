# using pygame.event.set_grab() in pygame

# This method holds or grab your cursor and keeps it inside your pygame window.

# Also this example uses windowleave and windowenter events. 

import pygame, sys

pygame.init()
screen = pygame.display.set_mode((700,300))
sr = screen.get_rect()
font = pygame.font.SysFont('Century Gothic',30)
text = font.render('Press Space, please :D', True, 'gold', 'brown')
tr = text.get_rect(center =(sr.center))

screen.blit(text, tr)
pygame.display.update(tr)


while True:
    # you can optimize your programs by just passing the events you will need as a parameter of event.get
    for event in pygame.event.get([256, pygame.KEYDOWN, pygame.WINDOWLEAVE, pygame.WINDOWENTER]):
      if event.type == 256: # weird way to check for pygame.QUIT
         pygame.quit()
         sys.exit()

      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          if pygame.event.get_grab():
              pygame.event.set_grab(False)
              text = font.render("•••", True, 'gold')
              pygame.draw.rect(screen,'black',tr)
              tr = text.get_rect(center= sr.center)
              screen.blit(text, tr)
              pygame.display.flip() # each time we make a change to the screen, we need to flip/update our screen.
              pygame.display.set_caption(f'set_grab({pygame.event.get_grab()})')              
          else:
              pygame.event.set_grab(True)
              text = font.render("      I got you >:D\n Do not press space", True, 'gold', 'brown')
              pygame.draw.rect(screen,'black',tr)
              tr = text.get_rect(center= sr.center)
              screen.blit(text, tr)
              pygame.display.flip() 
              pygame.display.set_caption(f'set_grab({pygame.event.get_grab()})')

      if event.type == pygame.WINDOWLEAVE:
          text = font.render("Where are you going?", True, 'gold', 'brown')
          pygame.draw.rect(screen,'black',tr)
          tr = text.get_rect(center= sr.center)
          screen.blit(text, tr)
          pygame.display.flip()
      elif event.type == pygame.WINDOWENTER:
          if pygame.event.get_grab() is False:
            text = font.render("Press Space, please :D", True, 'gold', 'brown')
            pygame.draw.rect(screen,'black',tr)
            tr = text.get_rect(center= sr.center)
            screen.blit(text, tr)
            pygame.display.flip()
