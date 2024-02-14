# To make this, i took reference here:
# https://github.com/pygame/pygame/blob/main/examples/aacircle.py


import pygame
import pygame.gfxdraw


def aa_circle(surf:bool):
  # Basic pygame stuff you should be familiar with.
  pygame.init()
  screen_surface = pygame.display.set_mode((500, 500))
  screen_surface.fill('white')
  pygame.display.set_caption('aacircle explanation')

  # This surface is a "copy" of our screen surface (↑), but we need the SRCALPHA flag,
  # so surface (↓) can respect both color and transparency values, and then our white
  # background is going to be visible.
  if surf:
    surface = pygame.Surface(screen_surface.get_size(), pygame.SRCALPHA)
  else:
     surface = None

  # Drawing circles with diferent radius: We are passing the parameter radius*2,
  # in our first cycle, we are passing 0*2 wich is equal to 0,
  # so our circle will not be drawn, our for loop looks like this:
  # (0: 0*2=0,  1: 1*2=2,  2: 2*2=4,  3: 3*2=6... and so on).
  for radius in range(100):
      pygame.gfxdraw.aacircle(surface or screen_surface, 250, 250, radius*2, (173,255,47))

  # Blitting surface and updating the screen.
  if surface:
    screen_surface.blit(surface, (0, 0))
  pygame.display.flip()

  while True:
      # Commonly, we see a for loop to check for events, right?,
      # you can learn more of pygame.event.wait here -> [i will add a link here]
      e = pygame.event.wait()
      if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
          break
  pygame.quit()


# When False, the circles are going to be drawn directly onto screen_surface.
# When True, the circles are going to be drawn onto surface, then onto screen_surface.
  
# Using one or the other makes the circles look a little different 
# in our program, or what you think? 
aa_circle(False) 
