import pygame as pg

# basic setup
pg.display.init()
pg.font.init()
w,h = pg.display.get_desktop_sizes()[0]
window = pg.Window('stickmans', (w-200,h-200), pg.WINDOWPOS_CENTERED, resizable=True)
screen = window.get_surface()
sc = screen.get_rect()

# func to create a stickman
def create_stickman(key='topleft', pos=(0,0), size=(5,3), color='red', alpha=80, flag=0, label=None):
    main_surf = pg.Surface((sc.w/size[0], sc.h/size[1]), flag)
    main_rect = main_surf.get_rect()

    radius = min(main_rect.w, main_rect.h)//7
    # head
    pg.draw.circle(main_surf, color, (main_rect.w//2, radius), radius)
    # body
    pg.draw.line(main_surf, color, 
                (main_rect.w/2, radius*2-2), 
                (main_rect.w/2, main_rect.h/3+int(main_rect.h/7*1.5)), radius//2)
    # booty
    pg.draw.circle(main_surf, color, 
                  (main_rect.w/2+1, main_rect.h/3+int(main_rect.h/7*1.5)), radius//4)
    # left arm
    pg.draw.line(main_surf, color, 
                (main_rect.w/2+radius//4, radius*2), 
                (main_rect.right-main_rect.w/3, main_rect.h/3+int(main_rect.h/7*1.5)), radius//4)
    # right arm
    pg.draw.line(main_surf, color, 
                (main_rect.w/2-radius//4, radius*2), 
                (main_rect.w/3, main_rect.h/3+int(main_rect.h/7*1.5)), radius//4)
    # left leg 
    pg.draw.line(main_surf, color,
                (main_rect.w/2-1+main_rect.h//130, main_rect.h/3+int(main_rect.h/7*1.5)), 
                (main_rect.right-main_rect.w/3, main_rect.h), radius//4)
    # right leg
    pg.draw.line(main_surf, color,
                (main_rect.w/2+1-main_rect.h//130, main_rect.h/3+int(main_rect.h/7*1.5)),
                (main_rect.w/3, main_rect.h), radius//4)
    # getting the distance between the legs wich are the 2 furthest points on the surface
    stickw = main_rect.w/3-main_rect.h//130
    # creating a subsurface with only the size that is needed
    r = (stickw, 0,main_rect.w-stickw*2-1,main_rect.h)
    s = main_surf.subsurface(*r)
    r = s.get_rect()
    # fast implemetation of labels
    if label:
        if ';' in label:
          fsize, color, label = label.split(';',2)
          if ',' in color:
             color = color.replace('(','')
             color = color.replace(')','')
             color = tuple(color.split(','))
          fsize = r.w // len(fsize) // int(fsize)
          f = pg.font.SysFont('centurygothic', fsize)
          label = f.render(label, True, color, wraplength=s.get_width())
          label_rect = label.get_rect(center= r.center)
          s.blit(label, label_rect)
    s.set_alpha(alpha)
    # this able us to grab the stickman.center (rect properties) and place that point onto another
    exec(f"r.{key} = {pos}")
    return s,r 


# lets have fun creating stickmans of diferent sizes !!
def create_stickmans():
    stickmans = [
        create_stickman(label='5;gold;Default'),
        create_stickman('center', (sc.centerx/3, sc.centery), (10,5), 'blue', label='5;brown;pos=1/3'),
        create_stickman('center', sc.center, (1,1), 'green', label='5;cyan;size=(1,1)'),               
        create_stickman('center', (sc.width-sc.centerx//3, sc.centery), (5,2), 'orange', label='5;white;Click for fullscreen'),               
                ]
    return stickmans


# draw all the args (functions -> [(pg.surface.Surface, pg.rect.Rect)]) that we pass 
def draw(*args):
    args = [*args]
    screen.fill('grey5')
    for func in args:
      screen.blits(func())
    window.flip()  


draw(create_stickmans)
running = True
clock = pg.time.Clock()
pg.event.clear()
while running:
  e = pg.event.wait()
  if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
      running = False
  elif e.type == pg.WINDOWRESIZED:
      sc = screen.get_rect()
      draw(create_stickmans)
  elif e.type == pg.MOUSEBUTTONDOWN:
      if window.size == (w,h):
        window.size = (w-200,h-200)
        window.position = pg.WINDOWPOS_CENTERED
        sc = screen.get_rect()
        draw(create_stickmans)
      else:
        window.position = (0,0)
        window.size = (w,h)
        sc = screen.get_rect()
        draw(create_stickmans)
  elif e.type == pg.VIDEORESIZE:
      #print(e.size)
      ...
  clock.tick(30)/1000
pg.quit()
