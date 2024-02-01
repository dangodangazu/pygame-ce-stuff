import pygame

pygame.init() # this initialize all the stuff you will need
screen = pygame.display.set_mode((400,300)) # create your pygame window, (400 width, 300 height)
pygame.display.set_caption('Opening a pygame window') # give your program a title
clock = pygame.time.Clock() # this will be usefull to: get how many fps your program is running,
                            # limit how many fps your program will run, and more.

running = True
while running:
  # This for loop and pygame method, will help you to check for events, suchs as:
  #   keyborad inputs 
  #   mouse inputs 
  #   window events
  for event in pygame.event.get():
    if event.type == pygame.QUIT: # This, constantly checks if you click on [x] icon (topright of your pygame window).
      running = False             # if you did, quits pygame, and running will be False.
   screen.fill('white')           # fills the screen in a white color.
   pygame.display.flip()          # updates the screen so we can see the changes when we changed our screen color.
  clock.tick(60)/1000             # limits fps to 60.  
pygame.quit() 
