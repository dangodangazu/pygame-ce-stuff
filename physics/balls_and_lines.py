"""

To make this, i took reference here:
 https://github.com/viblo/pymunk/blob/master/pymunk/examples/balls_and_lines.py
 
"""

import pygame, pymunk
from pygame.locals import *
from sys import exit as sys_exit

class Window: 
  def __init__(self, screen_w:int, screen_h:int, fullscreen=False, caption='Pygame Examples',):

    #  GET USER SCREEN SIZE, IDK IF THIS WILL ALWAYS WORK  #
    self.desktop_w = pygame.display.get_desktop_sizes()[0][0]
    self.desktop_h = pygame.display.get_desktop_sizes()[0][1]

    if fullscreen:
      #↓ ↓ ↓ ↓ FULLSCREEN ↓ ↓ ↓ ↓
      self.screen_w = self.desktop_w
      self.screen_h = self.desktop_h
    else:
      # DEFINE OTHER SIZE FOR THE SCREEN #
      self.screen_w = screen_w
      self.screen_h = screen_h

    self.screen = pygame.display.set_mode((self.screen_w, self.screen_h)) #OUR FINAL SCREEN SIZE
    self.screen_rect = self.screen.get_rect() #GET THE RECT OF OUR WINDOW
    
    pygame.display.set_caption(caption) #ESTABLISH A CAPTION


class Event_handler: #NEVER USE THIS WAY OF HANDLING EVENTS MAYBE
    def __init__(self, *keys) -> None:
        self.actions = {key: False for key in keys}
        self.mouse = None
        self.mouse_pos = None

    def handle_events(self,event):
      if event.type == QUIT:
        self.quit_game()
      if event.type == KEYDOWN:
        self.__keydown(event)
      if event.type == KEYUP:
        self.__keyup(event)
      if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
          self.mouse = (event.pos,1)
      if event.type == MOUSEMOTION:
        self.mouse_pos = event.pos


    def __keydown(self, event):
        for key in self.actions:
            if event.key == getattr(pygame.locals, f"K_{key}"):
                self.actions[key] = True
    
    def __keyup(self, event):
        for key in self.actions:
            if event.key == getattr(pygame.locals, f"K_{key}"):
                self.actions[key] = False

    def quit_game(self):
        pygame.quit()
        sys_exit()


# This is the actual class that does pymunk stuff
class Space:
  def __init__(self, screen: pygame.surface.Surface, gravity=(0,-800)) -> None:
    self.space = pymunk.Space()
    self.space.gravity = gravity
    self.lines = [] # our list that will contain our line shapes so we can draw them
    self.circles = [] #our list that will contain our circle shapes and bodies we will draw later 
    self.screen = screen
    self.screen_rect = self.screen.get_rect()
    self.circle_counter = 0
    # If you have a very small monitor, you might need to move this positions of the following "boxes"
    # because i didn't have desktop size too much in consideration when creating this lines, or boxes
    self.create_line((100,100), (200,100))
    self.create_line((100,200), (100,100))
    self.create_line((200,200), (100,200))
    self.create_line((200,200), (200,100))
    self.create_box()
    self.create_box(pos= (500,500))
    self.create_box(pos= (500,500))
    self.create_box(pos= (800,300), scale=100)
    self.create_circle((200,0))
    self.create_instructions()
    self.display_instructions = True
    #defining the keys we will use in the simulation
    self.event_handler = Event_handler('LEFT', 'RIGHT', 'UP', 'DOWN', 'z', 'h', 'x', 'ESCAPE') 
    pygame.key.set_repeat(200, 50)


  def flipy(self,y): #INVERTS Y AXIS
    return -y+self.screen_rect.h
  

  def create_instructions(self): #yes, i didn't write a foor loop
    font = pygame.font.SysFont('Arial', 15)
    self.text = font.render('Press arrow keys to change gravity', True, 'black')
    self.text2 = font.render('L-Click to drop a ball', True, 'black')
    self.text3 = font.render('Press z to erase some balls', True, 'black')
    self.text4 = font.render('Press h to hide those text', True, 'black')
    self.text5 = font.render('Press x to create a bunch of balls', True, 'black')
    self.text6 = font.render('Press escape to exit', True, 'black')


  def render_instructions(self): #yes, i didn't write a foor loop
    if self.display_instructions:
      self.screen.blit(self.text,(0,0))
      self.screen.blit(self.text2, (0,15))
      self.screen.blit(self.text3, (0,30))
      self.screen.blit(self.text5, (0,45))
      self.screen.blit(self.text4, (0,60))
      self.screen.blit(self.text6, (0,75))



  def debug(self, info, x=10, y=10):
    font = pygame.font.SysFont('Arial', 15)
    debug_surf = font.render(str(info),True, "white")
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(self.screen, "black", debug_rect)
    self.screen.blit(debug_surf, debug_rect)



  def create_line(self, start_pos, end_pos, color='red'):
    start = pymunk.Vec2d(start_pos[0], self.flipy(start_pos[1]))
    end = pymunk.Vec2d(end_pos[0], self.flipy(end_pos[1]))
    line = pymunk.Segment(self.space.static_body, start, end, 0.0)
    line.color = color
    self.space.add(line)
    self.lines.append(line)



  def create_box(self, scale=200, pos=(300,300)):
    self.create_line((pos[0],pos[1]), (pos[0]+scale, pos[1]))
    self.create_line((pos[0],pos[1]+scale), (pos[0], pos[1]))
    self.create_line((pos[0]+scale,pos[1]+scale), (pos[0], pos[1]+scale))
    self.create_line((pos[0]+scale, pos[1]), (pos[0]+scale, pos[1]+scale))


  def draw_line(self):
    if self.lines:
      for line in self.lines:
        body = line.body
        pv1 = body.position + line.a
        pv2 = body.position + line.b
        p1 = int(pv1.x), int(self.flipy(pv1.y))
        p2 = int(pv2.x), int(self.flipy(pv2.y))
        pygame.draw.line(self.screen, line.color, (p1), (p2))


  def create_circle(self, pos, radius=10, color=(249,200,200,180)):
    p = pos[0], self.flipy(pos[1])
    body = pymunk.Body(10, 100)
    body.position = p
    circle = pymunk.Circle(body, radius, (0, 0)) #this is our shape
    circle.friction = 0.5
    circle.color = color #color for each circle
    self.space.add(body, circle) #we add our body and our shape
    self.circles.append(circle) # we just add a circle to our list for drawing 
    self.circle_counter +=1


  def draw_circles(self):
    if self.circles:
      for circle in self.circles:
        v = circle.body.position
        rot = circle.body.rotation_vector
        p = v.x, self.flipy(v.y)
        #p2 = p + pymunk.Vec2d(rot.x, -rot.y) * ball.radius * 0.9
        p2 = p + pymunk.Vec2d(rot.x, -rot.y) * circle.radius
        p2 = int(p2.x), int(p2.y)
        self.destroy_circle_if_goes_outside_the_screen(circle, p)
        pygame.draw.circle(self.screen, circle.color, p, int(circle.radius))
        pygame.draw.line(self.screen, 'red', p, p2)


  def erase_circles(self):
    for circle in self.circles:
      self.erase_circle(circle)


  def erase_circle(self, circle):
      if self.circles:
        self.circles.remove(circle)
        self.space.remove(circle)
        self.space.remove(circle.body)
        self.circle_counter-=1


  def destroy_circle_if_goes_outside_the_screen(self, circle, pos):
      p = pos
      if p[1] > self.screen_rect.h+circle.radius or p[1]<0-circle.radius:
        self.erase_circle(circle)
      elif p[0] > self.screen_rect.w+circle.radius or p[0]<0-circle.radius:
        self.erase_circle(circle)
    

  def update(self):
    for event in pygame.event.get():
      self.event_handler.handle_events(event)
    if self.event_handler.actions['LEFT']:
      self.space.gravity = (-800, 0)
    if self.event_handler.actions['RIGHT']:
      self.space.gravity = (800,0)
    if self.event_handler.actions['UP']:
      self.space.gravity = (0,800)
    if self.event_handler.actions['DOWN']:
      self.space.gravity = (0,-800)
    if self.event_handler.actions['z']:
      self.erase_circles()
    if self.event_handler.actions['h']:
      if self.display_instructions:
        self.display_instructions = False
    if self.event_handler.mouse:
      self.create_circle(self.event_handler.mouse[0])
      self.event_handler.mouse = None
    if self.event_handler.actions['x']:
      for _ in range(7):
        self.create_circle(self.event_handler.mouse_pos)
    if self.event_handler.actions['ESCAPE']:
      self.event_handler.quit_game()
      

  def render(self,dt,fps):
    self.screen.fill((100,100,100))
    self.draw_line()
    self.draw_circles()
    self.render_instructions()
    self.debug(f'BALLS: {self.circle_counter}',0,self.screen_rect.h-20)
    self.debug(f'FPS: {fps}',0,self.screen_rect.h-40)
    self.space.step(dt)


class Game:
  def __init__(self, fullscreen=False, fps_limit=60, w=500,h=500, caption='Game', icon=None) -> None:
    pygame.init()
    self.state_stack = []
    self.fps_limit = fps_limit

    self.window = Window(w,h,fullscreen, caption)

    self.screen = self.window.screen
    self.screen_rect = self.window.screen_rect

    self.space = Space(self.screen)
    self.state_stack.append(self.space)

    self.clock = pygame.time.Clock()


  def update(self):
    self.state_stack[-1].update()


  def render(self):
    self.state_stack[-1].render(self.dt, self.fps)
    pygame.display.flip()



  def run(self):
    while True:
      self.dt = self.clock.tick(self.fps_limit)/1000
      self.fps = self.clock.get_fps()
      self.update()
      self.render()




if __name__ == '__main__':
    game = Game(1,caption='Physics example') #configure the options you desire.
    game.run()

