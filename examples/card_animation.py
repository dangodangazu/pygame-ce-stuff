import pygame
from random import choice

# Basic setup
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('card animation')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Century Gothic',30)

# Creating the symbols and colors for our cards
texts = [
         '♥', '○', '↓', 
         '♦', '♣', '▬',
         '♪', '\(•_•)/',
         '♠', '◘', '♫'
         ]

colors = [
          'orange', 'lime', 'greenyellow', 
          'yellow', 'grey', 'burlywood', 'brown', 
          'black', 'lightgrey', 'burlywood4', 'darkblue' 
          ]


def create_card():
  s = pygame.Surface(screen.get_size())
  color = choice(colors)
  t = choice(texts)
  colors.remove(color) # removing cards and color 
  texts.remove(t)      # so choice can't choose them anymore
  text = font.render(t, True, 'white')
  s.fill(color)
  s.blit(text, text.get_rect(center= (400,200)))
  r = s.get_rect(topleft = (s.get_width(), 0))
  return s, r
  
  
def move_card_to_the_left(rect, speed):
  if rect.x>0: 
    rect.x-=speed*dt
  if rect.x<0:
    rect.x = 0
    pygame.time.set_timer(MOVE_LAYER, 0) # This disables the event
  return pygame.Rect(rect.x, rect.y, rect.w, rect.h)


MOVE_LAYER = pygame.event.custom_type() #UserEvent.
s = None
bg = 'black'
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False
      if event.key == pygame.K_LEFT:
        bg = screen.get_at((0,0))
        if texts:
          s, r = create_card()
        pygame.time.set_timer(MOVE_LAYER, 1)
    if event.type == MOVE_LAYER:
      pygame.event.set_blocked(pygame.KEYDOWN) # blocks keydown 
      r = move_card_to_the_left(r, 340)        # to avoid K_LEFT spam
      if r.x == 0: pygame.event.set_allowed(pygame.KEYDOWN)
  if s:
    screen.blit(s, r)
  pygame.display.flip()
  dt = clock.tick(60)/1000     
pygame.quit()
