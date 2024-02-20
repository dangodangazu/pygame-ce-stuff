import pygame

class TextBox:
    def __init__(self, pos, w,h, color, bg_color): 
        self.screen = pygame.display.get_surface()
        self.text = ''
        # self.font = pygame.font.Font('assets/Z_PS2P.ttf', 20) # load a font  
        self.font = pygame.font.SysFont('Century Gothic', 30)
        self.pos = pos
        self.w = w
        self.h = h

        self.color = color
        self.bg_color = bg_color
        pygame.key.set_repeat(200, 50)


    def update(self, event):
          if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
          if event.type == pygame.TEXTINPUT:
              self.text += event.text


    def render(self):
        text_box = pygame.Rect(self.pos[0],self.pos[1],self.w,self.h)
        text_surface = self.font.render(self.text, True, self.color, None, text_box.width)
        pygame.draw.rect(self.screen,(self.bg_color), text_box)
        self.screen.blit(text_surface,(self.pos))           


class Game:
    def __init__(self,fullscreen=False, screen_w=800, screen_h=600,fps=60,) -> None:
        pygame.init()
        self.running = True
        self.desktop_w = pygame.display.get_desktop_sizes()[0][0]
        self.desktop_h = pygame.display.get_desktop_sizes()[0][1]
        if fullscreen:
            self.screen_w = self.desktop_w
            self.screen_h = self.desktop_h
        else:
            self.screen_w = screen_w
            self.screen_h = screen_h
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.text_box = TextBox((0, 0), 400,400, 'white', 'orange')

    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.text_box.update(event)
            
            
    def render(self):
        self.text_box.render()
        pygame.display.flip()
    

    def run(self):
        while self.running:
            self.update()
            self.render()
            self.dt = self.clock.tick(self.fps)

              
if __name__ == '__main__':
    game = Game(0, fps=30)
    game.run()
