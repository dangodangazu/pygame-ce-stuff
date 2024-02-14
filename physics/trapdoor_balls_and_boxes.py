
# https://github.com/BIGPOLLOWO/pygame-ce-collection


import pygame, pymunk
from pygame.locals import *
from random import randint, choice
from sys import exit as sys_exit


class Window: 
  def __init__(self, screen_w:int, screen_h:int, fullscreen=False, caption='Game', icon=None):

    #  OBTENER LAS MEDIDAS DE PANTALLA DEL USUARIO  #
    self.desktop_w = pygame.display.get_desktop_sizes()[0][0]
    self.desktop_h = pygame.display.get_desktop_sizes()[0][1]

    if fullscreen:
      #↓ ↓ ↓ ↓ JUEGO EN PANTALLA COMPLETA ↓ ↓ ↓ ↓
      self.screen_w = self.desktop_w
      self.screen_h = self.desktop_h
    else:
      # DEFINE OTRAS MEDIDAS PARA LA PANTALLA DE EL JUEGO  #
      self.screen_w = screen_w
      self.screen_h = screen_h

    #Es el resultado final de las  medidas de pantalla
    self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), vsync=True)
    self.screen_rect = self.screen.get_rect()
    
    pygame.display.set_caption(caption) #Se pone una caption para la ventana de pygame

    if icon:
      icon = pygame.image.load(icon).convert_alpha()
      pygame.display.set_icon(icon) #Si se proveyó un ícono, entonces se pondrá el ícono a la ventana


class Event_handler: #NEVER USE THIS WAY OF HANDLING EVENTS MAYBE
    def __init__(self, *keys) -> None:
        self.actions = {key: False for key in keys}
        self.actions_once = {}
        for key, item in self.actions.items():
           self.actions_once[key]=item

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
          self.mouse = event.pos
          print(event.pos)


    def __keydown(self, event):
        for key in self.actions:
            if event.key == getattr(pygame.locals, f"K_{key}"):
                self.actions[key] = True
                self.actions_once[key] = True
    
    def __keyup(self, event):
        for key in self.actions:
            if event.key == getattr(pygame.locals, f"K_{key}"):
                self.actions[key] = False

    def quit_game(self):
        pygame.quit()
        sys_exit()


class Game:
    def __init__(self, fullscreen=False, screen_w=500, screen_h=500, fps_limit=60, caption='physics example #2') -> None:
      pygame.init()
      self.window = Window(screen_w, screen_h, fullscreen, caption)
      self.screen = self.window.screen
      self.screen_rect = self.window.screen_rect
      self.fps_limit = fps_limit
      self.state_stack = []
      self.space = Space(self)
      self.state_stack.append(self.space)
      self.clock = pygame.time.Clock()


    def render(self):
       self.state_stack[-1].render()
       pygame.display.flip()
       

    def update(self):
       self.state_stack[-1].update()


    def run(self):
       while True:
          self.dt = self.clock.tick(self.fps_limit)/1000
          self.fps = self.clock.get_fps()
          self.update()
          self.render()
              


class Space:
    def __init__(self, game) -> None:
        self.game = game
        self.event_handler = Event_handler('x','z','q','SPACE','ESCAPE','LEFT', 'RIGHT', 'UP', 'DOWN','1','2', '3')
        self.actions = self.event_handler.actions
        self.actions_once = self.event_handler.actions_once

        self.space = pymunk.Space()
        self.space.gravity = (0,-800)
        self.screen = game.screen
        self.circles = []
        self.lines = []
        self.gates = []
        self.gates_directions = []
        self.removed_gates = []
        self.gates_open = False
        self.segments = {'lines':self.lines,'gates':self.gates}

        self.create_line((self.screen.get_width()//2, self.screen.get_height()//2-100), (self.screen.get_width()//2,self.screen.get_height()//2+200),'lines','yellow')
        self.create_open_box((self.screen.get_width()//2-100, self.game.screen_rect.h-30-100-1),200,100,'lines','blue')
        
        self.create_line((0,self.game.screen_rect.h-30), (self.game.screen_rect.w, self.game.screen_rect.h-30),'lines')
        self.create_box((100,100), 400,100, gate=4,alt_color='black', open_direction='left')
        self.count = 0
        self.ball_thrown = False
        self.pause_simulation = False
        self.display_mode = 1

        self.circle_counter = 0
        self.down_counter = 0
        self.up_counter = 0
        self.left_counter = 0
        self.right_counter = 0

        self.color_list = []
        self.color_list = [(249,200,200,180), (255,255,255)] # opcion de color 1
        self.color_list = [(220,77,79), (77,22,80)]
        self.color_list = [(35,4,80), (35,32,80), (35,52,80), (35,131,80),(35,165,180),(35,202,80)]
        #self.color_list = [(randint(0,255),randint(0,255),randint(0,255)), 
        #                  (randint(0,255),randint(0,255),randint(0,255))] #opcion de color 3

        self.display_instructions = False
        self.create_instructions()
        self.f = pygame.font.SysFont('Arial', 15)
        self.t = self.f.render('Press q to see controls',True,'white','black')
        self.t_rect = self.t.get_rect(topleft =(self.game.screen_rect.topleft))
        self.c = 0
        

    def create_instructions(self): #yes, i didn't write a foor loop
        f = pygame.font.SysFont('Arial', 15)
        self.text = f.render('Press arrow keys to change gravity, x for 0 gravity', True, 'white','black')
        self.text2 = f.render('L-Click to set a mouse position', True, 'white','black')
        self.text3 = f.render('Press z to create a shape', True, 'white','black')
        self.text4 = f.render('Press space to open a container', True, 'white','black')
        self.text6 = f.render('Press 1 | 2 | 3 to change display mode', True, 'white','black')
        self.text5 = f.render('Press escape to exit', True, 'white','black')

  
    def debug(self, info, x=10, y=10):
      debug_surf = self.f.render(str(info),True, "white")
      debug_rect = debug_surf.get_rect(topleft = (x,y))
      pygame.draw.rect(self.screen, "black", debug_rect)
      self.screen.blit(debug_surf, debug_rect)

    def render_instructions(self):
      if self.display_instructions:
        self.screen.blit(self.text,(0,0))
        self.screen.blit(self.text2, (0,15))
        self.screen.blit(self.text3, (0,30))
        self.screen.blit(self.text4, (0,45))
        self.screen.blit(self.text6, (0,60))
        self.screen.blit(self.text5, (0,75))


    def render_debug(self):
        self.debug(f'FPS: {int(self.game.clock.get_fps())}',self.game.screen_rect.x, self.game.screen_rect.h-45)
        self.debug(f'SHAPES: {self.circle_counter}', self.game.screen_rect.x, self.game.screen_rect.h-30)
        self.debug(f'GRAVITY: {int(self.space.gravity[0]),int(self.space.gravity[1])}', self.game.screen_rect.x, self.game.screen_rect.h-15)


    def flipy(self,y): #INVERTS Y AXIS
      return -y+self.game.screen_rect.h
    

    def create_line(self, start_pos, end_pos, key, color='red'):
      start = pymunk.Vec2d(start_pos[0], self.flipy(start_pos[1]))
      end = pymunk.Vec2d(end_pos[0], self.flipy(end_pos[1]))
      line = pymunk.Segment(self.space.static_body, start, end, 0.0)
      line.color = color
      line.elasticity = 1
      self.space.add(line)
      self.segments[key].append(line)
      
    
    def create_box(self, pos, width, height, color='black',gate=None,open_direction=None,alt_color=None): 
        if gate:
          if open_direction:
            self.gates_directions.append(open_direction)
          if alt_color is None:
             alt_color = color
          if gate == 1:
             self.create_line((pos[0], pos[1]), (pos[0]+width, pos[1]), 'gates', alt_color)
             self.create_line((pos[0], pos[1]), (pos[0], pos[1]+height), 'lines', color)
             self.create_line((pos[0]+width, pos[1]), (pos[0]+width, pos[1]+height), 'lines', color)
             self.create_line((pos[0], pos[1]+height), (pos[0]+width, pos[1]+height), 'lines', color)
          elif gate == 2:
             self.create_line((pos[0], pos[1]), (pos[0]+width, pos[1]), 'lines', color)
             self.create_line((pos[0], pos[1]), (pos[0], pos[1]+height), 'gates', alt_color)
             self.create_line((pos[0]+width, pos[1]), (pos[0]+width, pos[1]+height), 'lines', color)
             self.create_line((pos[0], pos[1]+height), (pos[0]+width, pos[1]+height), 'lines', color)
          elif gate == 3:
             self.create_line((pos[0], pos[1]), (pos[0]+width, pos[1]), 'lines', color)
             self.create_line((pos[0], pos[1]), (pos[0], pos[1]+height), 'lines', color)
             self.create_line((pos[0]+width, pos[1]), (pos[0]+width, pos[1]+height), 'gates', alt_color)
             self.create_line((pos[0], pos[1]+height), (pos[0]+width, pos[1]+height), 'lines', color)
          elif gate == 4:
             self.create_line((pos[0], pos[1]), (pos[0]+width, pos[1]), 'lines', color)
             self.create_line((pos[0], pos[1]), (pos[0], pos[1]+height), 'lines', color)
             self.create_line((pos[0]+width, pos[1]), (pos[0]+width, pos[1]+height), 'lines', color)
             self.create_line((pos[0], pos[1]+height), (pos[0]+width, pos[1]+height), 'gates', alt_color)       
        else:
          key = 'lines'               
          #1. line from topleft to topright
          self.create_line((pos[0], pos[1]), (pos[0]+width, pos[1]), key, color)
          #2. line from topleft to bottomleft
          self.create_line((pos[0], pos[1]), (pos[0], pos[1]+height), key, color)
          #3. line from topright to bottomright
          self.create_line((pos[0]+width, pos[1]), (pos[0]+width, pos[1]+height), key, color)
          #4. line from bottomleft to bottomright
          self.create_line((pos[0], pos[1]+height), (pos[0]+width, pos[1]+height), key, color)


    #we can say open_gates and close_gates work, but gates cannot really have diferent directions to open.
          # to make this work i did append or remove the gate, each time space key was pressed,
          # when it removes, then save the postion of the segment to create the same line again later.
    def open_gates(self): 
        if self.gates_directions:
          for i, direction in enumerate(self.gates_directions):
                  gate = self.segments['gates'][i]
                  gate_w = gate.b.x-gate.a.x
                  
                  if direction == 'left':
                      new_end = pymunk.Vec2d(gate.a.x+gate_w-50, self.flipy(gate.a.y-gate_w/2))
                      self.create_line((gate.a.x, self.flipy(gate.a.y)), new_end, 'gates', gate.color)

                  # Remove the existing gate segment
                  pos = ((gate.a.x, self.flipy(gate.a.y)),(gate.b.x, self.flipy(gate.b.y)))
                  gate.pos = pos
                  self.removed_gates.append((pos, direction))
                  self.space.remove(gate)
                  self.gates_directions.remove(direction)
                  self.gates.remove(gate)
          self.gates_open = True


    def close_gates(self):
       if not self.gates_directions:
          for pos, direction in self.removed_gates:
             self.space.remove(self.gates.pop())
             self.create_line(pos[0], pos[1], 'gates', 'black')
       self.gates_directions.append(direction)
       self.gates_open = False  
             

    def create_open_box(self, pos, width, height, key, color):
       #2. line from topleft to bottomleft
       self.create_line((pos[0], pos[1]), (pos[0], pos[1]+height), key, color)
       #3. line from topright to bottomright
       self.create_line((pos[0]+width, pos[1]), (pos[0]+width, pos[1]+height), key, color)
       #4. line from bottomleft to bottomright
       self.create_line((pos[0], pos[1]+height), (pos[0]+width, pos[1]+height), key, color)
       
                  
    def draw_line(self):
      if self.segments['lines']:
        for line in self.segments['lines']:
          body = line.body
          pv1 = body.position + line.a
          pv2 = body.position + line.b
          p1 = int(pv1.x), int(self.flipy(pv1.y))
          p2 = int(pv2.x), int(self.flipy(pv2.y))
          pygame.draw.line(self.screen, line.color, (p1), (p2))


    def draw_gates(self):
      if self.segments['gates']:
        for line in self.segments['gates']:
          body = line.body
          pv1 = body.position + line.a
          pv2 = body.position + line.b
          p1 = int(pv1.x), int(self.flipy(pv1.y))
          p2 = int(pv2.x), int(self.flipy(pv2.y))
          pygame.draw.line(self.screen, line.color, (p1), (p2))


    def append_circle(self):
            if self.actions['z']:
                self.mx, self.my = self.event_handler.mouse or (100,100)
                for _ in range(3):
                   if _ == 2:
                      self.create_circle((self.mx, self.my), randint(9,10))                   
                   else:
                      self.create_circle((self.mx, self.my), randint(1,5))
   
    
    def inputs(self):
        # cheking if mousebutton down and key z
        self.append_circle()
        # keys down, up, left and right changes the gravity
        if self.actions['DOWN']:
            self.down_counter-=0.1
            wind, grav = self.space.gravity[0], self.space.gravity[1]
            grav+= self.down_counter
            self.space._set_gravity((wind, grav))
        elif self.actions['UP']:
            self.up_counter+=0.1
            wind, grav = self.space.gravity[0], self.space.gravity[1]
            grav+= self.up_counter
            self.space._set_gravity((wind, grav))
        elif self.actions['LEFT']:
            self.left_counter -= 0.1
            wind, grav = self.space.gravity[0], self.space.gravity[1]
            wind += self.left_counter           
            self.space._set_gravity((wind, grav))  
        elif self.actions['RIGHT']:
            self.right_counter += 0.1
            wind, grav = self.space.gravity[0], self.space.gravity[1]
            wind += self.right_counter           
        # set the gravity to (0,0)
        elif self.actions['x']:
            self.space._set_gravity((0,0))
        elif self.actions['ESCAPE']:
            self.event_handler.quit_game()
        elif self.actions_once['SPACE']:
             self.actions_once['SPACE'] = False
             if self.gates_open:
               self.close_gates()
             else:
               self.open_gates()
        # display modes
        elif self.actions['1']:
           self.display_mode = 1
        elif self.actions['2']:
           self.display_mode = 2
        elif self.actions['3']:
           self.display_mode = 3
        # controls
        if self.actions['q']:
           self.c = 500
           self.display_instructions = True
        else:
           self.display_instructions = False


    def create_circle(self, pos, radius=10):
      p = pos[0], self.flipy(pos[1])
      body = pymunk.Body(10, 100)
      body.position = p
      circle = pymunk.Circle(body, radius, (0, 0)) #this is our shape
      circle.friction = 0.5
      circle.elasticity = 0.40
      circle.color = (randint(0,255),randint(0,255),randint(0,255)) #color for each circle
      circle.surface = pygame.Surface((radius*2, radius*2)).convert()
      circle.surface.fill(choice(self.color_list))
      self.space.add(body, circle) #we add our body and our shape
      self.circles.append(circle) # we just add a circle to our drawing list as well
      self.circle_counter +=1


    def draw_circles(self):
      if self.circles:
        for circle in self.circles:
          v = circle.body.position
          rot = circle.body.rotation_vector
          p = v.x, self.flipy(v.y)
          p_center = v.x-circle.radius, self.flipy(v.y+circle.radius) #fix the pos for display mode 3          
          p2 = p + pymunk.Vec2d(rot.x, -rot.y) * circle.radius*0.9
          p2 = p2.x, p2.y
          self.destroy_circle_if_goes_outside_the_screen(circle, p) #self explanatory

          if self.display_mode == 1:
            pygame.draw.circle(self.screen, circle.color, p, int(circle.radius))
            if self.actions['z']:
              pygame.draw.circle(self.screen, choice(self.color_list), (self.mx,self.my), 10)
              #pygame.draw.line(self.screen, 'black', p, p2) # it does a cool effect to just blit the radius as well         
          elif self.display_mode == 2:
             pygame.draw.circle(self.screen, circle.color, p, circle.radius)
             pygame.draw.line(self.screen, 'black', p, p2)         
             if self.actions['z']:
              pygame.draw.circle(self.screen, choice(self.color_list), (self.mx,self.my), 10)
          elif self.display_mode == 3:
            self.screen.blit(circle.surface, p_center) # alternatively you can draw rects with circle physics lol
            
          
    def erase_circle(self, circle):
        if self.circles:
          self.circles.remove(circle)
          self.space.remove(circle)
          self.space.remove(circle.body)
          self.circle_counter-=1


    def erase_circles(self):
      for circle in self.circles:
        self.erase_circle(circle)


    def destroy_circle_if_goes_outside_the_screen(self, circle, pos):
        p = pos
        if p[1] > self.game.screen_rect.h+circle.radius or p[1]<0-circle.radius:
          self.erase_circle(circle)
        elif p[0] > self.game.screen_rect.w+circle.radius or p[0]<0-circle.radius:
          self.erase_circle(circle)


    def update(self):
        for event in pygame.event.get():
           self.event_handler.handle_events(event)
        self.inputs()    
        self.c+=1


    def render(self):
        self.game.screen.fill((120,100,100))
        self.draw_line()
        self.draw_gates()
        self.space.step(self.game.dt)
        self.draw_circles()
        self.render_instructions()
        self.render_debug()
        if self.c < 500:
           self.screen.blit(self.t, self.t_rect)
        if self.c == 500:
           self.c = 500


if __name__ == '__main__':
   game = Game(1, caption='Trapdoor and boxes', fps_limit=100)
   game.run()
