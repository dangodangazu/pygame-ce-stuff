

# https://github.com/BIGPOLLOWO/pygame-ce-collection


FULLSCREEN = True

# if FULLSCREEN is true then you can ignore this: ↓ 

SCREEN_W, SCREEN_H = 1200, 600 # this will be your size if FULLSCREEN is False

# if you are not a windows user, you might be interested in changing the font: ↓

FONT = 'centurygothic'


import pygame as pg
import sys
from time import sleep
from random import randint, choice

# a single class that contains all the game logic
class UntitledClickerGame:
  def __init__(self, fullscreen:bool, screen_w=None, screen_h=None) -> None:
    pg.display.init()
    pg.font.init()
    if fullscreen:  w,h = pg.display.get_desktop_sizes()[0]
    else: w,h = screen_w, screen_h

    self.screen = pg.display.set_mode((w,h))    
    self.screen_ = self.screen.get_rect()
    pg.display.set_caption('untitled clicker game')
    s = pg.Surface((10,10))
    s.fill((35,165,180))
    pg.display.set_icon(s)
    del s
    self.colors = [(35, 4, 80), (35, 32, 80), (35, 52, 80), (35, 131, 80), (35, 165, 180), (35, 202, 80)]
    self.f = pg.font.SysFont(FONT, 25)
    self.f2 = pg.font.SysFont(FONT, 15)
    self.stuff = {}
    self.ran = 300

    self.counter = 60
    self.points = set()
    self.score = 0
    self.past_score = None
    self.best_score = 0

    self.try_again = False
    
    
  def debug(self, info, x=10, y=10):
    s = self.f.render(str(info), True, "black")
    r = s.get_rect(topleft=(x, y))
    self.screen.blit(s, r)


  def generate_map(self):
    w,h = self.screen.get_size()
    for i in range(self.ran):
        size = randint(20, 40)
        surf = pg.Surface((size, size))
        surf.fill(choice(self.colors))
        pos = randint(0, w - size), randint(0, h - size)
        rect = surf.get_rect(topleft=pos)
        t = self.f2.render(f'{i}', True, 'orange')
        tr = t.get_rect(center=rect.center)
        self.stuff[i] = {'surface': surf, 'rect': rect, 'direction': randint(100, 300), 'text':t, 'tr': tr, 'points':i}


  def intro_loop(self, delay=None):
    # text that will be displayed on diferent screens
    texts = [
    'Welcome!, this is a quick game example!',
    'The rules are simple',
    'A bunch of rectangles will appear on the screen',
    "Each rectangle will show its value at the beginning",
    "Click on the rectangles to win points",
    "Are you ready?"      
    ]

    # variables 
    screen = self.screen
    screen_ = self.screen_
    txt = self.f.render('Press enter to continue', True, 'black')
    txt_rect = txt.get_rect(center=(screen_.centerx, screen.get_height()-screen.get_height()/3))
    index = 0

    # loop 
    pg.event.clear()
    while True:
      screen.fill('white')
      t = self.f.render(texts[index], True, 'black')
      t_rect = t.get_rect(center = screen_.center)
      t.set_alpha(255)
      txt.set_alpha(255)
      screen.blit(t, t_rect)
      screen.blit(txt, txt_rect)
      pg.draw.line(screen, 'black', (txt_rect.x, txt_rect.bottom), (txt_rect.x + txt_rect.w, txt_rect.bottom))
      pg.display.flip()
      event = pg.event.wait()
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_RETURN:
          screen.fill('white')
          txt.set_alpha(100)
          txt.set_alpha(100)
          screen.blit(t, t_rect)
          screen.blit(txt, txt_rect)
          pg.display.flip()
          pg.time.wait(300)
          index += 1
          screen.fill('white')
          pg.display.flip()
          if index == len(texts):
            break
        if event.key == pg.K_ESCAPE:
          sys.exit()
    if delay:
      sleep(delay)


  def create_rects_loop(self, delay=None):
    # variables
    screen = self.screen
    screen_ = self.screen_
    p = ['.', '..', '...']
    index = 0

    # text surfaces and text rects
    txt = self.f.render('Creating rectangles', False, 'black')
    txt_rect = txt.get_rect(center=screen_.center)
    txt2 = self.f.render(p[index], False, 'black')
    txt2_rect = txt.get_rect(bottomleft=txt_rect.bottomright)
    counter = 0

    # loop
    pg.event.clear()
    for i in range(self.ran):
      event = pg.event.wait(20)
      if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        sys.exit()
      counter +=1
      if counter >= int(self.ran / 3):
          txt2 = self.f.render(p[index], False, 'black')
          txt2_rect = txt.get_rect(bottomleft=txt_rect.bottomright)
          index += 1
          counter = 0
      # blitting stuff
      screen.blit(self.stuff[i]['surface'], self.stuff[i]['rect'])
      screen.blit(self.stuff[i]['text'], self.stuff[i]['tr'])
      screen.blit(txt, txt_rect)
      screen.blit(txt2, txt2_rect)
      pg.display.update([self.stuff[i]['rect'], self.stuff[i]['tr'], txt_rect, txt2_rect])
      if event.type != pg.NOEVENT:
         sleep(0.020)
    if delay:
      sleep(delay)
  

  def threetwoone_loop(self, delay=None):
    # variables
    screen = self.screen
    screen_ = self.screen_
    ONE_SECOND = pg.event.custom_type()
    pg.time.set_timer(ONE_SECOND, 1000)
    counter = 3
    running = True

    # texts surfaces and rects 
    txt = self.f.render('3', True, 'red')
    txt2 = self.f.render('GO!', True, 'red')
    txt_rect = txt.get_rect(center=screen_.center)
    txt2_rect = txt2.get_rect(center=screen_.center)

    # while loop
    while running:
      for event in pg.event.get([ONE_SECOND, pg.QUIT, pg.KEYDOWN]):
        if event.type == ONE_SECOND:
            counter -= 1
            txt = self.f.render(f'{counter}', True, 'red')
            txt_rect = txt.get_rect(center=screen_.center)
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            sys.exit()
      # blitting everything
      screen.fill('white')
      for i in range(self.ran):
        screen.blit(self.stuff[i]['surface'], self.stuff[i]['rect'])
        screen.blit(self.stuff[i]['text'], self.stuff[i]['tr'])    
      if counter == 0:
        screen.blit(txt2, txt2_rect)
        pg.display.flip()
        if delay:
          sleep(delay)
        running = False
      else:
        screen.blit(txt, txt_rect)
      pg.display.flip()


  def game_loop(self, delay=None):
    # user events
    ONE_SECOND = pg.event.custom_type()
    GOTAPOINT = pg.event.custom_type()
    pg.time.set_timer(ONE_SECOND, 1000)

    def animate_point(rect,speed):
      rect.y-=speed*dt
      return rect
    
    # variables and a pgclock
    clock = pg.time.Clock()
    running = True
    r = None
    kill_rect = None
    kill_0 = False

    pg.event.clear()
    while running:
      dt = clock.tick(60) / 1000
      fps = clock.get_fps()
      for event in pg.event.get([pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.QUIT, ONE_SECOND, GOTAPOINT]):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
          running = False
        if event.type == ONE_SECOND:
          self.counter -= 1
        if event.type == GOTAPOINT:
          r = animate_point(txt_rect, 1)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
          for stuff in self.stuff.values():
            if stuff['rect'].collidepoint(event.pos):
              self.points.add(stuff['points'])
              kill_rect = stuff['points']
              txt = self.f.render(f'+{stuff["points"]}', True, 'green')
              txt_rect = txt.get_rect(center = stuff['tr'].center)
              pg.time.set_timer(GOTAPOINT, 2)
              if stuff['points'] == 0:
                kill_0 = True
              self.score = sum(list(self.points))
          if kill_rect:
            self.stuff.__delitem__(kill_rect)
          elif kill_0:
            self.stuff.__delitem__(0)
            kill_0 = False
          kill_rect = None
      self.screen.fill('white')
      for stuff in self.stuff.values():
        if stuff['rect'].right >= self.screen_.w:
            stuff['direction'] = -stuff['direction']
        if stuff['rect'].left <= 0:
            stuff['direction'] = abs(stuff['direction'])
        stuff['rect'].x += stuff['direction'] * dt
        stuff['tr'].x += stuff['direction'] * dt
        self.screen.blit(stuff['surface'], stuff['rect'])
        self.screen.blit(stuff['text'], stuff['tr'])
      self.debug(f'Time: {self.counter}')
      # uncomment this to see fps
      #self.debug(f'FPS: {fps}',y=35)
      if r:
        self.screen.blit(txt,r)
      pg.display.flip()
      if self.counter == 0:
        running = False
    if delay:
      sleep(delay)
    # disable user events
    pg.time.set_timer(ONE_SECOND,0)
    pg.time.set_timer(GOTAPOINT,0)


  def final_loop(self):
    # load an save score
    self.load_and_save_score()
    # text surfaces and rects
    pg.event.clear()
    txt = self.f.render(f'Your score was: {self.score}', True, 'black')
    txt_rect = txt.get_rect(center = self.screen_.center)
    txt2 = self.f.render('Try again?', True, 'black')
    txt2_rect = txt2.get_rect(center = (self.screen_.centerx/2, self.screen_.centery+self.screen_.centery/2)) 
    txt3 = self.f.render('Quit game ', True, 'black')
    txt3_rect = txt3.get_rect(center = (self.screen_.centerx+self.screen_.centerx/2, 
                                      self.screen_.centery+self.screen_.centery/2))

    text4 = self.f2.render(f'Best score: {self.best_score or self.score}', True,  'red')
    text4_rect = text4.get_rect(topleft = txt_rect.bottomleft)

    # drawing function    
    def draw(alpha_quit, alpha_try):
      self.screen.fill('white')
      self.screen.blit(txt, txt_rect)
      self.screen.blit(text4, text4_rect)
      txt2.set_alpha(alpha_try)
      self.screen.blit(txt2, txt2_rect)
      txt3.set_alpha(alpha_quit)
      self.screen.blit(txt3, txt3_rect)
      pg.draw.line(self.screen, 'black', (txt_rect.x, txt_rect.bottom), (txt_rect.x + txt_rect.w, txt_rect.bottom))
      pg.draw.line(self.screen, 'black', (txt2_rect.x, txt2_rect.bottom), (txt2_rect.x + txt2_rect.w, txt2_rect.bottom))
      pg.draw.line(self.screen, 'black', (txt3_rect.x, txt3_rect.bottom), (txt3_rect.x + txt3_rect.w, txt3_rect.bottom))
      pg.display.flip()
    draw(255,255)

    # while loop
    pg.event.clear()
    while True:
      event = pg.event.wait()
      if event.type == pg.KEYDOWN:
          if event.key == pg.K_ESCAPE:
              break
      elif event.type == pg.QUIT:
          break
      elif event.type == pg.MOUSEMOTION:
          if txt2_rect.collidepoint(event.pos):
              draw(255, 100)
          elif txt3_rect.collidepoint(event.pos):
              draw(100,255)
          else:
              draw(255,255)
      elif event.type == pg.MOUSEBUTTONUP:
          if txt2_rect.collidepoint(event.pos):
              self.try_again = True
              break
          elif txt3_rect.collidepoint(event.pos):
             if self.try_again:
                self.try_again = False
             break
  

  def load_and_save_score(self):
    # try to load
    try:
       with open('score.txt') as f:
          self.past_score = int(f.readline())   
    except:...
    # getting a highscore
    if self.past_score:
        if self.past_score > self.score:
          self.best_score = self.past_score
        elif self.past_score < self.score:
           self.best_score = self.score
        else: ...
    # saving  
    with open('score.txt', 'w') as f:
      f.write(f'{self.best_score or self.score}')


  def run(self):
     # call everything
     self.generate_map()
     self.intro_loop()
     self.create_rects_loop(1)
     self.threetwoone_loop(1)
     self.game_loop()
     self.final_loop()


  def again(self):
     # reset variables
     self.stuff = {}
     self.ran = 300
     self.counter = 60
     self.points = set()
     self.stuff = {}
     self.score = 0
     self.screen.fill('white')
     pg.display.flip()
     # call everything except intro 
     self.generate_map()
     self.create_rects_loop(1)
     self.threetwoone_loop(1)
     self.game_loop()
     self.final_loop()


if __name__ == '__main__':
   game = UntitledClickerGame(FULLSCREEN, SCREEN_W, SCREEN_H)
   game.run()
   # making a try again functionality
   while game.try_again:
      game.again()
   # quiting everything
   pg.display.quit()
   pg.font.quit()
