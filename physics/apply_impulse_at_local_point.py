import pymunk, pygame, sys


class Space:
  def __init__(self, impulse=None, gravity=(0,0)) -> None:
    
    self.space = pymunk.Space()
    self.space.gravity = gravity
    self.body = pymunk.Body(1,10)
    self.shape = pymunk.Circle(self.body, 10)
     
    if impulse:
      self.impulse = pymunk.Vec2d(impulse[0], impulse[1])
      x = impulse[0]
      y = impulse[1]
      x = -x
      y = -y  
      self.opposite_impulse = pymunk.Vec2d(x,y)
    else:
      self.impulse = None


  def add_circle_to_space(self, func):
    if self.body not in self.space.bodies:
      self.space.add(self.body, self.shape)
      func(f"A body has been added to the space, your impulse force is: {self.impulse}", 10, 70)

  def apply_local_impulse(self):
    if self.impulse:
      self.body.apply_impulse_at_local_point(self.impulse)


  def apply_opposite_impulse(self):
    if self.impulse:
      self.body.apply_impulse_at_local_point(self.opposite_impulse)

  def run(self, dt):
    self.space.step(dt)


pygame.init()
screen = pygame.display.set_mode((700,300))
pygame.display.set_caption('Apply local impulse')
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial',20)

def debug(info, x=10, y=10):
  surf = font.render(str(info),True, "white")
  rect = surf.get_rect(topleft = (x,y))
  pygame.draw.rect(screen, "black", rect)
  screen.blit(surf, rect)

# An object at rest remains at rest, and an object in motion remains in motion at constant speed 
# and in a straight line unless acted on by an unbalanced force.  
space = Space((-100,0),(0,0)) # (impulse,gravity) 

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_z:
        space.add_circle_to_space(debug)
      elif event.key == pygame.K_x:
        space.apply_local_impulse()
      elif event.key == pygame.K_c:
        space.apply_opposite_impulse()

  pygame.draw.rect(screen, 'black', (0,0,700,40))
  debug(f'POSITION: {space.shape.body.position}')
  debug('Press z to add the body, x to apply an impulse, c to apply an opposite impulse', 10, 40)

  dt = clock.tick(60)/1000
  space.run(dt)       
  pygame.display.update((0,0,700,95))
  
