import pygame as pg

# basic setup
pg.init()
screen = pg.display.set_mode((500, 500), pg.RESIZABLE)
screen_ = screen.get_rect()
pg.display.set_caption('Half-Responsive desing and RESIZABLE window flag')
f = pg.font.SysFont('centurygothic', 20)

# usefull function to create and position a text surface
def ftxt(text:str, key='topleft', ref=screen_.topleft, color='black'): 
    """
    Fast Text:
    - grabs the point "key" of "text" and places it on the point "ref"
    - returns a tuple -> (pygame.Surface, pygame.Rect)
    """
    
    s = f.render(text, True, color)
    r = s.get_rect()
    exec(f"r.{key} = {ref}")
    return (s,r)

# list that contains all texts with diferent positions and
# placing the point topleft of the text onto the point topleft of the window, and so on...
def txt_list():  
    texts = [
            ftxt('I am on the topleft (↑←)'),
            ftxt('topright (↑→)', 'topright', 'screen_.topright'),
            ftxt('bottomleft (↓←)', 'bottomleft', 'screen_.bottomleft'),
            ftxt('bottomright (↓→)', 'bottomright', 'screen_.bottomright'),
            ftxt('I am on the center (x)', 'center', 'screen_.center'),
            ]
    return texts


# appending a new text, but now we take a position from texts instead of the screen_ 
# +10 value gives an offset the the y position
def txt_list_update(texts):
    texts.append(ftxt('i am below of a rect that is on the center!', 
                      'center', 
                      (texts[4][1].centerx,texts[4][1].bottom+10), 
                      'red'))
    return texts

# draws everything
def draw():
    global screen_
    screen_ = screen.get_rect()
    screen.fill('white')
    texts = txt_list()
    texts = txt_list_update(texts)
    screen.blits(texts)
    pg.display.flip()

draw()

# while loop
running = True
while running:
    event = pg.event.wait()
    if event.type == pg.QUIT or event.type == pg.KEYDOWN:
        running = False
    if event.type == pg.WINDOWRESIZED:
        draw()
pg.quit()


#  methods:
#    • pg.init
#    • pg.display.set_mode
#    • surface.get_rect
#    • pg.font.SysFont
#    • pg.display.set_caption
#    • font.render
#    • surface.fill
#    • surface.blits
#    • pg.display.flip
#    • pg.event.wait
#    • pg.quit
# 
#  events:
#    • QUIT
#    • KEYDOWN
#    • WINDOWRESIZED
#
#  flags:
#    • RESIZABLE
