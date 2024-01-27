import pygame
from pygame.locals import *

screen = pygame.display.set_mode((300,400))


screen.fill((100,100,100))
line = pygame.draw.line(screen,'red',(100,100), (199,100)) 
line2 = pygame.draw.rect(screen, 'blue', (100,200,100,1))
line3 = pygame.Surface((100,1)) 
line3.fill('yellow')
screen.blit(line3, (100, 300))
pygame.display.update()

print(line)
print(line2)
print(line3.get_rect())

running = True

while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
      if event.type == MOUSEBUTTONDOWN:
        print(event.pos)
    dt=pygame.time.Clock().tick(60)/1000    
    
