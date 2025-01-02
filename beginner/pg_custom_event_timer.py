#example of how to create a timer using a custom event
import pygame as pg

# basic setup 
pg.init()
screen = pg.display.set_mode((500, 500))
screen_ = screen.get_rect()
clock = pg.time.Clock()
pg.display.set_caption('pg.event.custom_type()')
running = True

# timer and custom event
CUSTOM_EVENT = pg.event.custom_type()
TIMER_ON = False
TIME = 0

# text rendering functions
f = pg.font.SysFont('centurygothic', 80)
fsmall = pg.font.SysFont('centurygothic', 25)
fsmaller = pg.font.SysFont('centurygothic', 15)
def ftxt_constant_call(text, key='topleft', ref='screen_.topleft', color='black', antia=True, bgcolor=None):
    s = f.render(str(text), antia, color,bgcolor)
    r = s.get_frect()
    exec(f"r.{key} = {ref}")
    screen.blit(s, r)

def ftxt(text:str, key='topleft', ref='screen_.topleft', 
        color='white', wrap=None, 
        alpha=255, bgcolor=None, font=None) -> tuple[pg.Surface, pg.Rect]: 
    s = font.render(text, True, color, wraplength=wrap or 0, bgcolor=bgcolor)
    s.set_alpha(alpha)
    r = s.get_rect()
    exec(f"r.{key} = {ref}")
    return (s,r)
txt = ftxt('Press space to start/stop the timer', 'midtop', [screen_.midtop[0], screen_.midtop[1]+15], font=fsmall, color='black')
txt2 = ftxt('Press esc to exit as always', 'midbottom', [screen_.midbottom[0], screen_.midbottom[1]-15], font=fsmaller, color='black')


# while loop
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    # timer stuff
            if event.key == pg.K_SPACE:
                if TIMER_ON:
                    TIMER_ON = False
                    pg.time.set_timer(CUSTOM_EVENT, 0)
                else:
                    TIMER_ON = True
                    pg.time.set_timer(CUSTOM_EVENT, 1000)
        if event.type == CUSTOM_EVENT:
            TIME+=1
            
    #drawing
    screen.fill('white')
    ftxt_constant_call(TIME, 'center', screen_.center)
    screen.blit(*txt)
    screen.blit(*txt2)
    clock.tick(60)
    pg.display.flip()
pg.quit()
