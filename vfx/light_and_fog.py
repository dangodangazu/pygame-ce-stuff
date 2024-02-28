import pygame as pg

pg.init()
screen = pg.display.set_mode((728,455), pg.WINDOWPOS_CENTERED)
screen_ = screen.get_rect()
screen_copy = pg.Surface(screen.get_size())
wallpaper = pg.image.load('wallpaper.jpg').convert()
pg.mouse.set_visible(0)

def generate_glow(glow, radius):
  # create a surf
  surf = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
  layers = 25
  # restricting the glow between 0 to 255
  for i in range(layers):
    k = i*glow
    k = pg.math.clamp(k,0,255)
    pg.draw.circle(surf, (k,k,k), surf.get_rect().center, radius-i*3)
  return surf

def loop(draw, caption, pos):
  pg.display.set_caption(caption)
  while True:
    e = pg.event.wait()
    if e.type == pg.QUIT:
      raise SystemExit()
    elif e.type == pg.MOUSEMOTION:
      pos = e.pos
    elif e.type == pg.KEYDOWN:
      if e.key == pg.K_ESCAPE:
        break
    draw(pos)
    pg.display.flip()
  return pos

def draw_one(pos):
  screen.blit(wallpaper,(0,0))
  screen_copy.fill('black')
  screen_copy.blit(surf, (pos[0]-100, pos[1]-100), special_flags=pg.BLEND_RGB_MAX)
  screen.blit(screen_copy, (0,0), special_flags=pg.BLEND_RGB_MULT)

def draw_two(pos):
  screen.blit(wallpaper,(0,0))
  screen_copy.blit(surf, (pos[0]-100, pos[1]-100), special_flags=pg.BLEND_RGB_MAX)
  screen.blit(screen_copy, (0,0), special_flags=pg.BLEND_RGB_MULT)


surf = generate_glow(10,100)
pos = loop(draw=draw_one, caption='VFX - LIGHT', pos=(0,0))
loop(draw=draw_two, caption='VFX - LIGHT + FOG', pos=pos)
pg.quit()
