# MIT License

# Copyright (c) 2024 bigpollowo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This is a hangman game that gets a word from the website:
# 'https://en.wikipedia.org/wiki/Cat'
# you can place any other website you want 
# and the program will attempt to return 
# all words from that website.

# Note: There are still things to polish
# like drawing the letters that the user
# already tried to guess in the game,
# maybe add one extra life for the 
# stickman because the game is a bit 
# complicated right now, and make
# better graphics, maybe some day
# i will comeback and add more stuff.

import pygame as pg
import requests
import re
from bs4 import BeautifulSoup
from random import choice
from sys import exit as sys_exit

FULLSCREEN = True
FONT = 'centurygothic'
BGCOLOR = 'grey5'
FONTCOLOR = 'white'

class Hangman:
    def __init__(self, fullscreen:bool, caption:str, screen_w=None, screen_h=None,) -> None:
        pg.display.init()
        pg.font.init()
        if fullscreen:  w,h = pg.display.get_desktop_sizes()[0]
        else: w,h = screen_w, screen_h
        #w, h = w-200, h-200
        self.screen = pg.display.set_mode((w,h))    
        self.screen_ = self.screen.get_rect()
        pg.display.set_caption(caption)
        
        self.f_mini = pg.font.SysFont(FONT, 12)
        self.f = pg.font.SysFont(FONT, 25)
        self.f_underlined = pg.font.SysFont(FONT, 25)
        self.f_underlined.set_underline(True)

        self.url = self.choose_url()
        self.words = None
        self.connected = None

        body_parts = ['head', 'body', 'arml', 'armr', 'legl', 'legr']
        pg.display.set_icon(self.draw_stickman('topleft', (0,0), (3,5), 'black', pg.SRCALPHA, 255, 'surface', *body_parts))


    @staticmethod
    def choose_url():
        urls = [
          # ptilocichla and thryophilus are examples of words that are on wikipedia, so carefull there
          # some websites return 0 words so they are useless to play
          # place one or many urls here
          'https://en.wikipedia.org/wiki/Cat',
        ]

        # this websites return 0 words...
        #   "https://genshin.hoyoverse.com/es/"
        #   "https://www.contexto.me"
        #   "https://www.youtube.com"
        #   "https://www.pokedle.net"
        return choice(urls)


    @staticmethod
    def correct_words_output(txt):
        """This corrects the outputs for our words we got from the website"""
        words = re.findall(r'\b\w+\b', txt.lower())
        words_to_remove = set()
        vips = 'qwertyuiopasdfghjklñzxcvbnmáíóúé' #áâãàçéêíóôõú
        letters_with_vip_access = set()
        for i in vips:
            letters_with_vip_access.add(i)            
        for word in words:
            if len(word) >3:
                for c in word:
                    if c not in letters_with_vip_access:
                        words_to_remove.add(word)
                        break
            else: words_to_remove.add(word)                  

        
        # ugly stuff 
        for word in words:
          if 'aa' in word:
            words_to_remove.add(word)
          if 'eee' in word:
            words_to_remove.add(word)
          if 'ii' in word:
            words_to_remove.add(word)
          if 'ooo' in word:
            words_to_remove.add(word)
          if 'uu' in word:
            words_to_remove.add(word)
          if 'qq' in word:
            words_to_remove.add(word)  
          if 'ww' in word:
            words_to_remove.add(word)  
          if 'rrr' in word:
            words_to_remove.add(word)  
          if 'ttt' in word:
            words_to_remove.add(word)  
          if 'yy' in word:
            words_to_remove.add(word)  
          if 'ppp' in word:
            words_to_remove.add(word)  
          if 'sss' in word:
            words_to_remove.add(word)  
          if 'ddd' in word:
            words_to_remove.add(word)  
          if 'fff' in word:
            words_to_remove.add(word)  
          if 'ggg' in word:
            words_to_remove.add(word)  
          if 'hhh' in word:
            words_to_remove.add(word)  
          if 'jj' in word:
            words_to_remove.add(word)  
          if 'kk' in word:
            words_to_remove.add(word)  
          if 'll' in word:
            words_to_remove.add(word)  
          if 'zzz' in word:
            words_to_remove.add(word)  
          if 'xx' in word:
            words_to_remove.add(word)  
          if 'ccc' in word:
            words_to_remove.add(word)  
          if 'vv' in word:
            words_to_remove.add(word)  
          if 'bbb' in word:
            words_to_remove.add(word)  
          if 'nnn' in word:
            words_to_remove.add(word)  
          if 'mmm' in word:
            words_to_remove.add(word)
          if 'https' in word:
            words_to_remove.add(word)
                
        words = set(words)-words_to_remove
        return list(words)
       

    @staticmethod
    def create_glow(glow, radius):
      surf = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
      circles = 25
      for i in range(circles):
        v = i*glow
        v = pg.math.clamp(v,0,255)
        pg.draw.circle(surf, (v,v,v), surf.get_rect().center, radius-i*3)
      return surf


    def connect_to_website(self):
        # 1. Realizar la solicitud HTTP
        # 2. Verificar si la solicitud fue exitosa (código de estado 200)
        # 3. Obtener la lista de palabras de la página, luego corregir el output
        # 4. si la solicitud no fue exitosa simplemente imprime un mensaje de error
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.connected = True
                soup = BeautifulSoup(response.text, 'html.parser')
                txt = soup.get_text()
                self.words = self.correct_words_output(txt)
                #print(self.words)
                #print(txt)
                #print('lang=' in soup)
                #print(self.words)
                if self.words is None:
                    print(f"\033[91m The website: {self.url} returned 0 words!.\033[0m")
        except:
            self.connected = False
            print(f"""\033[91mSomething went wrong...
        1. Verify that you have internet connection.
        2. Check if the website: "{self.url or 'None'}" exist and if it is not down.
        3. Try again\033[0m""")

    # code formating of github somehow broke... oh well
    def ftxt(self, text:str, key='topleft', ref='self.screen_.topleft', color=FONTCOLOR, underlined=False, wrap=None, alpha=255, bgcolor=None, mini=False): 
        """
        Fast Text:
        - grabs the point "key" of "text" and places it on the point "ref"
        - returns a tuple -> (pygame.Surface, pygame.Rect)
        """
        
        if underlined: s = self.f_underlined.render(text, True, color, wraplength=wrap or 0)
        elif mini: s = self.f_underlined.render(text, True, color, wraplength=wrap or 0, bgcolor=bgcolor)
        else: s = self.f.render(text, True, color, wraplength=wrap or 0, bgcolor=bgcolor)
        s.set_alpha(alpha)
        r = s.get_rect()
        exec(f"r.{key} = {ref}")
        return (s,r)


    def title_screen(self):
        pg.event.clear()
        def draw(alpha):
            texts = [
            self.ftxt('HangMan', 'center', self.screen_.center),
            self.ftxt('Press enter to continue', 
                      'center',
                      (self.screen_.centerx, self.screen.get_height()-self.screen.get_height()/3),
                      underlined=True, alpha=alpha)]            
            self.screen.fill(BGCOLOR)
            self.screen.blits(texts)
            pg.display.flip()
        draw(255)
        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                sys_exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys_exit()
                if event.key == pg.K_RETURN:
                    draw(100)
                    pg.time.wait(300)
                    break


    def second_screen(self):
        pg.event.clear()
        sc = self.screen_
        b = self.ftxt(self.url, 'center', sc.center, 'blue', True)
        if b[1].w>sc.w:
            b = self.ftxt('link is too large to display', 'center', sc.center, 'blue', True)
        a = self.ftxt('You will connect to the following website:', 'center', (b[1].centerx, b[1].top-25))
        c = self.ftxt('Do you want to proceed?', 'center', (b[1].centerx, b[1].bottom+25))
        d = self.ftxt('Yes :D', 'center', (sc.centerx/3, sc.centery+sc.centery/2))
        e = self.ftxt('No :C', 'center', (sc.w-sc.w/6, sc.centery+sc.centery/2))
        def draw(alpha1, alpha2, alpha3):
            d[0].set_alpha(alpha1)
            e[0].set_alpha(alpha2)
            b[0].set_alpha(alpha3)
            blit_list = [a, b, c, d, e]
            self.screen.fill(BGCOLOR)
            self.screen.blits(blit_list)
            pg.display.flip()        
        draw(255,255,255)
        while True:
            ev = pg.event.wait()
            if ev.type==pg.QUIT or (ev.type==pg.KEYDOWN and ev.key==pg.K_ESCAPE): sys_exit()
            elif ev.type == pg.MOUSEMOTION:
                if d[1].collidepoint(ev.pos):
                    draw(100,255,255)
                elif e[1].collidepoint(ev.pos):
                    draw(255,100,255)
                elif b[1].collidepoint(ev.pos):
                    draw(255,255,100)
                else:
                    draw(255,255,255)
            elif ev.type == pg.MOUSEBUTTONUP:
                if ev.button == 1:
                    if d[1].collidepoint(ev.pos):
                        pg.time.wait(300)
                        break
                    elif e[1].collidepoint(ev.pos):
                        sys_exit()


    def third_screen(self):
        pg.event.clear()
        sc = self.screen_
        a = self.ftxt('Establishing connection', 'center', sc.center, 'red')
        def draw(alpha=255):
            self.screen.fill(BGCOLOR)
            self.screen.blit(*a)
            if self.connected:
                b[0].set_alpha(alpha)
                self.screen.blit(*b)
            pg.display.flip()
        draw()
        self.connect_to_website()
        b = self.ftxt('Play' if self.words else 'Quit', 'center', (sc.centerx, sc.h-sc.h/3), FONTCOLOR, True)
        if self.connected:
          a = self.ftxt(f'Connection established: \n{len(self.words)} words have been returned!', 
                        'center', sc.center, 'green', 1)
          if len(self.words)== 0:
              a = self.ftxt('Connection established\nbut 0 words have been returned', 'center', sc.center, 'gold')
        else:
          a = self.ftxt('Connection has failed', 'center', sc.center, 'red')
          draw()
          event = pg.event.wait(5000)
          if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
              sys_exit()
        draw()
        pg.event.clear()
        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                sys_exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys_exit()
                if event.key == pg.K_RETURN:
                    break
            elif event.type == pg.MOUSEMOTION:
                if b[1].collidepoint(event.pos):
                    draw(100)
                else:
                    draw(255)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.words:
                        if b[1].collidepoint(event.pos):
                            break
                    else: sys_exit()
    

    def select_difficulty(self):
        def draw(blits:list):
            self.screen.fill(BGCOLOR)
            self.screen.blits(blits)
            pg.display.flip()

        def create_texts(c1='black', c2='black', c3='black'):
            sc = self.screen_
            return [
            self.ftxt('Easy', 'center', (sc.centerx, sc.centery/2), c1, True, False, 255),
            self.ftxt('Medium', 'center', sc.center, c2, True, False, 255) ,
            self.ftxt('Hard', 'center', (sc.centerx, sc.centery+sc.centery/2), c3, True, False, 255)  
            ]
        
        def get_n_of_words_for_each_difficulty():
            easy_words = []
            medium_words = []
            hard_words = []

            for word in self.words:
                if len(word) == 4:
                    easy_words.append(word)
                elif 4 < len(word) < 7:
                    medium_words.append(word)
                elif len(word) > 6:
                    hard_words.append(word)

            return (easy_words, medium_words, hard_words)
        
        
        easy, m, h = get_n_of_words_for_each_difficulty()
        def create_box_info(difficulty, key, ref, color='white', bgcolor='grey5'):
            s, r = self.ftxt(f'{len(difficulty)} word entries in this difficulty', 
                             key, ref, color, bgcolor=bgcolor, mini=True)
            s.set_alpha(80)
            return [s,r]


        def idk(e,do_return=False):
                txts = create_texts()
                if txts[0][1].collidepoint(e.pos):
                    height = txts[0][1].h
                    #width = txts[0][1].w
                    txts = create_texts('green')
                    txts.append(create_box_info(easy, 'center',
                               (self.screen_.centerx, self.screen_.centery-self.screen_.centery/3+height)))
                    draw(txts)
                    if easy and do_return:
                       return ('easy', easy)
                elif txts[1][1].collidepoint(e.pos):
                    height = txts[1][1].h
                    #width = txts[1][1].w
                    txts = create_texts(c2='yellow')
                    txts.append(create_box_info(
                                m, 'center',
                               (self.screen_.centerx, self.screen_.centery+ self.screen_.centery/4)))
                    draw(txts)
                    if m and do_return:
                       return ('medium', m)
                elif txts[2][1].collidepoint(e.pos):
                    height = txts[2][1].h
                    #width = txts[2][1].w
                    txts = create_texts(c3='red')
                    txts.append(create_box_info(h, 'center',
                               (self.screen_.centerx, self.screen_.h-self.screen_.centery/5)))
                    draw(txts)
                    if h and do_return:
                       return ('hard', h)
                else:
                   draw(create_texts())
        draw(create_texts())
        pg.event.wait()
        while True:
            e = pg.event.wait()
            if e.type == pg.QUIT:
                sys_exit()
            elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                sys_exit()
            elif e.type == pg.MOUSEMOTION:
                idk(e)
            elif e.type == pg.MOUSEBUTTONUP:
                self.word_list = idk(e, True)
                if self.word_list:
                   self.difficulty = self.word_list[0]
                   self.word_list = self.word_list[1]
                   break
                   
    
    def hangman_loop(self):
        pg.event.clear()
        sc = self.screen_
        word = choice(list(self.word_list))
        l = len(word)
        

        def draw_pole():
            pg.draw.line(self.screen, 'black', 
                        (self.screen_.w//6, self.screen_.h//4),
                        (self.screen_.w//6, self.screen_.h//1.5),5)
            pg.draw.line(self.screen, 'black',
                        (self.screen_.w//12, self.screen_.h//1.5),
                        (self.screen_.w//4, self.screen_.h//1.5),5)
            pg.draw.line(self.screen, 'black',
                        (self.screen_.w//6, self.screen_.h//4),
                        (self.screen_.w//5, self.screen_.h//4), 5)
            pg.draw.line(self.screen, 'black',
                        (self.screen_.w//5, self.screen_.h//4),
                        (self.screen_.w//5, self.screen_.h//3), 5)
            return (self.screen_.w//5, self.screen_.h//3)
                     

        def create_lines(draw=True):
            start = sc.w//4+sc.w//20
            line_length = sc.w//20    
            if draw:                              
              for i in range(l):
                  x1, y1 = line_length*i+start, sc.h//1.5
                  x2, y2 = line_length*i+start+line_length//2, sc.h//1.5                  
                  pg.draw.line(self.screen, 'black', (x1, y1), (x2, y2))
            else:
              mid_points = []
              for i in range(l):
                  x1, y1 = line_length*i+start, sc.h//1.5
                  x2, y2 = line_length*i+start+line_length//2, sc.h//1.5
                  pg.draw.line(self.screen, 'black', (x1, y1), (x2, y2))
                  mx = x1+x2
                  mx /= 2
                  mid_points.append((mx, y1))
              return mid_points
        
        def draw_label(alpha, color='black'):
            txtsurf, txtrect = self.ftxt('Enter your response here', 'midbottom',               
                                        (self.screen_.centerx, self.screen_.h), color, 
                                          True, None, alpha)
            self.screen.blit(txtsurf, txtrect)
            return txtsurf, txtrect

        # variables that we will need
        mid_points = create_lines(0)
        body_parts = ['head', 'body', 'arml', 'armr', 'legl', 'legr']

        # creating the word surfaces that will be above the lines
        # and they will only be visible once the user guessed the full
        # word or a single letter of the whole word
        letters = []
        for i,c in enumerate(word):
            s = self.f.render(c,True,'black')
            r = s.get_rect(midbottom=(mid_points[i][0], mid_points[i][1]))
            letters.append((s,r))

        letters_blits = []

        def draw(alpha, color='blue', text_mode=False, get_input=False, event=None):
            self.screen.fill(BGCOLOR)
            hook = draw_pole()
            self.draw_stickman('midtop', hook, 
                              (5,3), 'blue', pg.SRCALPHA, 
                              80, 'radius', *body_parts)
            create_lines(1)
            draw_label(alpha, color)
            blits = []
            if text_mode:
                s_that_makes_the_screen_darker = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
                s_that_makes_the_screen_darker.fill('black')
                s_that_makes_the_screen_darker.set_alpha(200)
                text_input_rect = pg.Rect(0,0,sc.w/2, sc.h/10)
                text_input_rect.center = sc.center
                blits.append((s_that_makes_the_screen_darker, (0,0)))
                ok_surf, ok_rect = self.ftxt('OK','center', (sc.centerx/3, sc.centery+sc.centery/2),
                                             'green', True, None, 255, 'black')
                cancel_surf, cancel_rect = self.ftxt('Cancel', 'center', (sc.w-sc.w/6, sc.centery+sc.centery/2),
                                           'red',True, None, 255, 'black')
                blits.append((ok_surf, ok_rect))
                blits.append((cancel_surf, cancel_rect))
                if event:
                    if ok_rect.collidepoint(event.pos):
                        ok_surf.set_alpha(100)
                    elif cancel_rect.collidepoint(event.pos):
                        cancel_surf.set_alpha(100)
                    else:
                        cancel_surf.set_alpha(255)
                        ok_surf.set_alpha(255)
                blits.append(self.ftxt('Write a single letter or a word', 'center', (sc.centerx, sc.centery/3), 'white'))    
                pg.draw.rect(self.screen, 'blue', text_input_rect,5)
                for tup in letters_blits:
                    blits.append(tup)
                if get_input:
                    key_surf, key_rect = self.ftxt(keys, 'center',sc.center, 'white')
                    blits.append((key_surf, key_rect))
                self.screen.blits(blits)
                pg.display.flip()
                return text_mode, [ok_rect, cancel_rect]    
            else:
                for tup in letters_blits:
                    blits.append(tup)
                self.screen.blits(blits)          
                pg.display.flip()              

        keys=''
        guessed_a_key = False
        txtsurf, txtrect = draw_label(255)
        text_mode = False
        draw(255)
        # GAME
        while True:
            if text_mode:
                e = pg.event.wait()
                if e.type == pg.QUIT:
                    sys_exit()
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        sys_exit()
                    if e.key == pg.K_BACKSPACE:
                        keys = keys[:-1]
                        draw(255, text_mode=text_mode, get_input=1)  
                elif e.type == pg.TEXTINPUT:
                    keys+=e.text
                    draw(255, text_mode=text_mode, get_input=1)
                elif e.type == pg.MOUSEMOTION:
                    text_mode, rects = draw(255, text_mode=text_mode, get_input=1, event=e)
                elif e.type == pg.MOUSEBUTTONUP:
                    print(word)
                    guessed_a_key = False
                    if e.button == 1:
                        if rects[0].collidepoint(e.pos):
                            if keys == word:
                                self.won = True
                                break
                            else:
                                for i,c in enumerate(word):
                                    if c == keys[:1]:
                                        letters_blits.append(letters[i])
                                        guessed_a_key = True          
                                if guessed_a_key is False:
                                    body_parts.pop()

                                text_mode = 0
                                draw(255, text_mode=text_mode, get_input=0)
                                if len(letters_blits) == len(word):
                                    self.won = True
                                    break
                                if not body_parts:
                                    self.won = False
                                    break
                                keys = ''
                        elif rects[1].collidepoint(e.pos):
                            text_mode=0
                            draw(255,)
                            keys = ''
            else:    
                e = pg.event.wait()
                if e.type == pg.QUIT:
                    sys_exit()
                elif e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        sys_exit()
                elif e.type == pg.MOUSEMOTION:
                    if txtrect.collidepoint(e.pos):
                        draw(100)
                    else:
                        draw(255)
                elif e.type == pg.MOUSEBUTTONUP:
                    if e.button == 1:
                        if txtrect.collidepoint(e.pos):
                            text_mode, rects = draw(255, text_mode=True)


    def draw_final_screen(self):
        pg.event.clear()
        self.screen.fill(BGCOLOR)
        sc = self.screen_
        if self.won:
            self.screen.blit(*self.ftxt('You Won!', 'center', sc.center))
        else:
            self.screen.blit(*self.ftxt('You lose...', 'center', sc.center))
        pg.display.flip()
        while True:
            e = pg.event.wait()
            if e.type == pg.QUIT:
                sys_exit()
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    sys_exit()


    # func to create a stickman
    def draw_stickman(self,key, pos, size=(5,3), color='red', flag=pg.SRCALPHA, alpha=80, do_return='radius',*args):
        main_surf = pg.Surface((self.screen_.w/size[0], self.screen_.h/size[1]), flag)
        main_rect = main_surf.get_rect()
        radius = min(main_rect.w, main_rect.h)//7
        args = set(args)

        if 'head' in args:
            # head (circle)
            pg.draw.circle(main_surf, color, (main_rect.w//2, radius), radius)
        if 'body' in args:
            # body (line)
            pg.draw.line(main_surf, color, 
                   (main_rect.w/2, radius*2-2), 
                   (main_rect.w/2, main_rect.h/3+int(main_rect.h/7*1.5)), radius//2)
            # booty (circle)
            pg.draw.circle(main_surf, color, 
                          (main_rect.w/2+1, main_rect.h/3+int(main_rect.h/7*1.5)), radius//4)
        if 'arml' in args:
            # left arm (line)
            pg.draw.line(main_surf, color, 
                        (main_rect.w/2+radius//4, radius*2), 
                        (main_rect.right-main_rect.w/3, main_rect.h/3+int(main_rect.h/7*1.5)), radius//4)
        if 'armr' in args:
            # right arm (line)
            pg.draw.line(main_surf, color, 
                        (main_rect.w/2-radius//4, radius*2), 
                        (main_rect.w/3, main_rect.h/3+int(main_rect.h/7*1.5)), radius//4)
        if 'legl' in args:
            # left leg (line)
            pg.draw.line(main_surf, color,
                        (main_rect.w/2-1+main_rect.h//130, main_rect.h/3+int(main_rect.h/7*1.5)), 
                        (main_rect.right-main_rect.w/3, main_rect.h), radius//4)
        if 'legr' in args:
            # right leg (line)
            pg.draw.line(main_surf, color,
                        (main_rect.w/2+1-main_rect.h//130, main_rect.h/3+int(main_rect.h/7*1.5)),
                        (main_rect.w/3, main_rect.h), radius//4)
        # getting the distance between the legs wich are the 2 furthest points on the surface
        stickw = main_rect.w/3-main_rect.h//130
        # creating a subsurface with only the size that is needed
        r = (stickw, 0,main_rect.w-stickw*2-1,main_rect.h)
        s = main_surf.subsurface(*r)
        r = s.get_rect()
        s.set_alpha(alpha)
        # this able us to grab the stickman.center (rect properties) and place that point onto another
        exec(f"r.{key} = {pos}")
        self.screen.blit(s, r)
        if do_return == 'radius':
          return radius
        elif do_return == 'surface':
           return s


    def run(self):
       self.title_screen()
       self.second_screen()
       self.third_screen()
       self.select_difficulty()
       self.hangman_loop()
       self.draw_final_screen()


if __name__ == '__main__':
    game = Hangman(FULLSCREEN,'hangman')
    game.run()
