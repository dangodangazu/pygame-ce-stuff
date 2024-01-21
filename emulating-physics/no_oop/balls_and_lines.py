"""

Me: https://github.com/BIGPOLLOWO/pygame-ce-collection


To make this, i took reference here:
 https://github.com/viblo/pymunk/blob/master/pymunk/examples/balls_and_lines.py
 
 (mostly i just decomposed the code separating it 
 into functions to make it more readable, 
 and added my own things as well)

 to see a better version of this code, go to see my other example: 
 https://github.com/BIGPOLLOWO/pygame-ce-collection/blob/main/emulating-physics/balls_and_lines.py 
 
"""


# THIS EXAMPLE REQUIRES PYMUNK AND PYGAME-CE

#if you do not have pymunk or pygame-ce already installed

# GO TO THE TERMINAL AND TYPE  
#  pip install pymunk
#  pip install pygame-ce


import pygame, pymunk, sys
from pygame.locals import *

screen_w, screen_h = 300,300

pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))

font = pygame.font.SysFont('Arial', 15)
text = font.render('Press arrow keys to change gravity', True, 'black')
text2 = font.render('L-Click to drop a ball', True, 'black')
text3 = font.render('Press z to erase some balls', True, 'black')

def flipy(y):
  """This function makes gravity direction ↓ be negative and gravity direction ↑ be positive"""
  return -y+screen_h

space = pymunk.Space()
space.gravity = 0, -800

lines = []

def create_line(start_pos, end_pos):
  start = pymunk.Vec2d(start_pos[0], flipy(start_pos[1]))
  end = pymunk.Vec2d(end_pos[0], flipy(end_pos[1]))
  line = pymunk.Segment(space.static_body, start, end, 0.0)
  space.add(line)
  lines.append(line)

def draw_lines():
  for line in lines:
    body = line.body
    #pv1 = body.position + line.a.rotated(body.angle)
    pv1 = body.position + line.a
    #pv2 = body.position + line.b.rotated(body.angle)
    pv2 = body.position + line.b
    p1 = int(pv1.x), int(flipy(pv1.y))
    p2 = int(pv2.x), int(flipy(pv2.y))
    #pygame.draw.lines(screen, pygame.Color("lightgray"), False, [p1, p2])
    pygame.draw.line(screen, 'red', (p1), (p2))
    


circles = []


def create_circle(pos, radius=10):
  p = pos[0], flipy(pos[1])
  body = pymunk.Body(10, 100)
  body.position = p
  shape = pymunk.Circle(body, radius, (0, 0))
  shape.friction = 0.5
  shape.collision_type = 2
  space.add(body, shape)
  circles.append(shape)



def draw_circles():
  for circle in circles:
    v = circle.body.position
    rot = circle.body.rotation_vector
    p = int(v.x), int(flipy(v.y))
    p2 = p + pymunk.Vec2d(rot.x, -rot.y) * circle.radius * 0.9
    #p2 = p + pymunk.Vec2d(rot.x, -rot.y) * ball.radius
    p2 = int(p2.x), int(p2.y)
    pygame.draw.circle(screen, (249,200,200,180), p, circle.radius)
    pygame.draw.line(screen, 'red', p, p2)


def erase_circles():
  for circle in circles:
    circles.remove(circle)
    space.remove(circle)
    space.remove(circle.body)



#screen.fill('white')
create_line((100,100), (200,100))
create_line((100,200), (100,100))
create_line((200,200), (100,200))
create_line((200,200), (200,100))
create_circle((200,0))


running = True

while running:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == MOUSEBUTTONDOWN:
      if event.button == 1:
        create_circle(event.pos, 10)
    if event.type == KEYDOWN:
      if event.key == K_UP:
        space.gravity = (0,800)
      if event.key == K_DOWN:
        space.gravity = (0,-800)
      if event.key == K_LEFT:
        space.gravity = (-800,0)
      if event.key == K_RIGHT:
        space.gravity = (800,0)
      if event.key == K_z:
        erase_circles() # It will not erase every circle bodie and shape with one input because events 
                        # of pygame are True only for a certain amount of time after being pressed.
        print(space.bodies)
    
  screen.fill('white')
  draw_circles()
  draw_lines()
  screen.blit(text,(0,0))
  screen.blit(text2, (0,15))
  screen.blit(text3, (0,30))
  dt = pygame.time.Clock().tick(60)/1000
  space.step(dt)
  pygame.display.flip()
