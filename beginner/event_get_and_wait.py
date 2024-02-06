# This script is a brief explanation of how you could
# use pygame.event.wait() as another aproach of getting events.


#  pygame.event.get()
#    • On pygame examples, this way of getting events is very popular.
#    • Returns a list of all events in the event queue at that time.
#    • Most of the time, to not complicate things, you may need to use this method.
#
#   
#  pygame.event.wait()
#    • This method sort of blocks the program, so it doesn't consume CPU cycles while waiting.
#    • Returns a single event.
#    • If the queue is empty this function will wait until one is created.
#    • You can pass a timer as an argument (pygame 2.0.0), the timer will trigger the event NOEVENT    
#      when NOEVENT was triggered, the program will run again, if timer == 0 it will just wait until 
#      you trigger another event (Mouse events, keyboard events, window events, etc)

# basic setup
import pygame as pg
from time import time
pg.display.init()
pg.font.init()
screen = pg.display.set_mode((800,400))
screen_rect = screen.get_rect()
clock = pg.time.Clock()
f = pg.font.SysFont('Century Gothic',30)


def get_example():
  pg.display.set_caption('pygame.event.get()')
  # creating surfaces and their rects
  surf = pg.Surface((50,50))
  surf_rect = surf.get_rect()
  t = f.render('pygame.event.get()\n    our while loop\n  is always running', True, 'black')
  tr = t.get_rect(center = (400,200))
  t2 = f.render('Press any key to continue', True, (100,100,100))
  t2r = t2.get_rect(center = (400, screen.get_height()-60))
  # direction and speed we will need for our animation
  direction = 0
  speed = 450
  # usual while loop
  running = True
  cycles = 0
  while running:
    # our fps limiter, and we can use this to get a delta time as well
    dt =clock.tick(60)/1000
    c = f.render(f'Loop N°: {cycles}', True, 'black')
    cr = c.get_rect(bottomleft = (0, 400))
    # usual for loop
    for event in pg.event.get():
      e = event.type
      if e== pg.QUIT or e == pg.KEYDOWN or e == pg.MOUSEBUTTONDOWN:
        running=False
    # simple logic for our animation
    if surf_rect.left <= 0:
      direction = 1
    if surf_rect.right >= screen.get_width():
      direction = -1
    # blitting stuff
    screen.fill('white')
    surf_rect.x += direction*dt*speed
    screen.blit(surf, surf_rect)
    pg.draw.line(screen, 'red', (tr.centerx-200, tr.centery-15),(tr.centerx+200, tr.centery-15))
    screen.blit(t, tr)
    screen.blit(c, cr)
    screen.blit(t2, t2r)
    pg.display.flip()
    cycles+=1


def wait_example():
  # caption
  pg.display.set_caption('pygame.event.wait()')
  # creating a lot of surfaces (mostly text) and their rects
  s = pg.Surface((50,50))
  sr = s.get_rect()
  t = f.render('pygame.event.wait()\nour while loop will run\n    once per event', True, 'black')
  tr = t.get_rect(center = screen_rect.center)
  t2 = f.render('          (try to trigger events\nwith your mouse, keyboard, etc\n and left or right to modify timer)',True, 'black' )
  t2r = t2.get_rect()
  t3 = f.render('Press Enter to continue', True, (100,100,100))
  t3r = t3.get_rect(center = (screen_rect.centerx, screen.get_height()-60))
  c = f.render(f'Loop N°: 0', True, 'black')
  cr = c.get_rect(bottomleft = (0, 400))
  e = f.render(f'Event: {None}', True, 'black')
  er = e.get_rect(bottomright = (800,400))
  timer_surf = f.render(f'Timer: 0', True, 'black')
  timer_rect = timer_surf.get_rect(bottomleft= cr.topleft) 
  # variables
  direction = 0
  running = True
  cycles = 0
  timer = 0
  # blitting and updating everything just once outside our while loop
  # so we can see something in the screen
  screen.fill('white')
  screen.blit(t, tr)
  pg.draw.line(screen, 'red', (tr.centerx-200, tr.centery-15),(tr.centerx+200, tr.centery-15))
  screen.blit(t2, t2r)
  screen.blit(c, cr)
  screen.blit(e, er)
  screen.blit(timer_surf, timer_rect)
  screen.blit(s, sr)
  pg.display.flip()
  # if you used keydown pg.event.wait() will return KEYUP
  # or if you used mousebuttondown this will return mousebuttonup
  event = pg.event.wait()
  while running:
    # limit fps to 60 (we can't use this to get a dt now because
    # we are not going to cycle or while loop constantly anymore)
    clock.tick(60)/1000
    # the while loop is not going to go to the next line of code 
    # until you trigger an event here ↓
    event = pg.event.wait(timer)
    # using the time module to get a delta time,
    # pg.time.wait is a small hack to get a proper dt (we are waiting a millisecond)
    previous_time = time()
    pg.time.wait(1)
    dt = time()-previous_time
    # creating font surfaces and rects
    c = f.render(f'Loop N°: {cycles}', True, 'black')
    cr = c.get_rect(bottomleft = (0, 400))
    e = f.render(f'Event: {pg.event.event_name(event.type)}', True, 'black')
    er = e.get_rect(bottomright = (800,400))
    timer_surf = f.render(f'Timer: {timer}', True, 'black')
    timer_rect = timer_surf.get_rect(bottomleft= cr.topleft)  
    # check for events without needing a for loop
    if event.type == pg.QUIT:
      running = False
    elif event.type == pg.KEYDOWN:
      if event.key == pg.K_ESCAPE:
        running = False
      elif event.key == pg.K_RIGHT:
        timer+=10
      elif event.key == pg.K_LEFT:
        if timer>0:timer-=10
      elif event.key == pg.K_RETURN:
        running = False
    # simple logic for or animation
    if sr.left <= 0:
      direction = 1
    if sr.right >= screen.get_width():
      direction = -1
    sr.x += direction*dt*3000
    # blitting
    screen.fill('white')
    screen.blit(t, tr)
    pg.draw.line(screen, 'red', (tr.centerx-200, tr.centery-15),(tr.centerx+200, tr.centery-15))
    screen.blit(t2, t2r)
    screen.blit(c, cr)
    screen.blit(e, er)
    screen.blit(timer_surf, timer_rect)
    if cycles >300:
      screen.blit(t3, t3r)
    screen.blit(s, sr)
    pg.display.update()
    cycles+=1
  pg.display.quit()
  pg.font.quit()

# pg.event.get()
get_example()
# pg.event.wait()
wait_example()
