# This is a script that explains some very basic things about surfaces and rects, and more.
# I recommend you to run this script, and then to place your window to the side, or minimize it, 
# and that way you can read the code and take a look at the program, and therefore, it will be easier 
# to relate the code, with the looks of the program.

# Once you fully analized a section, you can close the window, 
# that will take you to the next section and another window will open.


import pygame, time


section1 = True
section2 = True
section3 = True



"""
||||||||||||||||||||||||||||||||||||||
  INTRODUCTION TO SURFACES AND RECTS
||||||||||||||||||||||||||||||||||||||
"""

if section1:
  pygame.init()
  screen = pygame.display.set_mode((400,300))
  screen_rect = screen.get_rect() #gets the rectangle of our surface

  pygame.display.set_caption('Surfaces and Rectangles') #sets a title to our program


  print(type(screen))  # -> <class 'pygame.surface.Surface'>
  print(type(screen_rect)) # -> <class 'pygame.rect.Rect'>

  # Surface
    #Is a pygame object for representing images
    #Surface((width, height), flags=0, depth=0, masks=None) -> Surface
    #Surface((width, height), flags=0, Surface) -> Surface


  # Rect
    #Is a pygame object for storing rectangular coordinates
    #Rect(left, top, width, height) -> Rect
    #Rect((left, top), (width, height)) -> Rect
    #Rect(object) -> Rect


  # ||||Surfaces and Rects are a very important part in pygame||||
  #         Surfaces:
  #           -Represents and "image".
  #           -Surfaces are a rectangular area of pixels.
  #           -Surfaces can be created or loaded.
  #           -You will need Surfaces to display images.
  #     
  #     
  #         Rects:
  #           -It stores rectangular coordinates.
  #           -Helps to place a Surface easily in the right spot.
  #           -Use rectangles for moving surfaces.
  #           -Useful for collision detection.
  
  
  # Surfaces containt everything you need to display an image.
  # Rectangles primarily stores those surface coordinates.


  # This is how you create a surface
  surf = pygame.Surface((40,40))  # -> <Surface(40x40x8)>

  # This is how you load a surface (use convert or convert alpha)
  try:
    surf2 = pygame.image.load('path_to_your_image/cute_tiny_cat.jpg').convert_alpha()
  except:
    print('--Image not found--')

  # This is a common way to create a Rect 
  # (notice we are just creating a new variable from a method of the surface we just created)

  surf_rect = surf.get_rect()


  # Once we got a surface, we can already display it
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    screen.fill('white') # Fills the screen in a white color -> (255,255,255)
    screen.blit(surf, (0,0)) # Displays our surf/black rectangle at the position (x=0, y=0) of our screen
    pygame.display.flip() # Updates the screen every single loop of our while loop
  pygame.quit()


  # What you saw was just a white screen, and a black surface.
  # Default color for surfaces is a black color, that's why our surface had a black color 
  # even if we did not provide a color.


  # Also notice how our surface was displayed at (x=0, y=0).
  # The position (x=0, y=0) on our screen as you can see, is at the topleft.
  # That means the starting point / (x=0, y=0), of every Surface is at the topleft.



  # ╔═════════════════════════════════════════════════════════════════════════════════════════╗
  # ║  You completed this section you can close the program, and continue with the next one.  ║
  # ╠═════════════════════════════════════════════════════════════════════════════════════════╣



"""
||||||||||||||||||||||||||||||||||||||
  AREAS AND SURFACES INSIDE SURFACES
||||||||||||||||||||||||||||||||||||||
"""
if section2:
  time.sleep(1)
  pygame.init()
  screen = pygame.display.set_mode((100,100)) # This is an area of 10000 pixels
  screen_rect = screen.get_rect()
  pygame.display.set_caption('Surfaces and Rectangles')

  font = pygame.font.SysFont('Century Gothic',10)
  text = font.render('arrow keys to move \nthe red one,\nwasd to move \nthe blinking rect', True, 'blue')
  text_rect = text.get_rect(center = screen_rect.center)

  # let's create a surface of (x=10px, y=10px)
  area_of_hundred_px = pygame.Surface((10,10), depth=8)
  # and a surfaces of (x=1,y=1)
  surface_of_one_px = pygame.Surface((1,1), depth=8)
  # getting their rects
  r_h = area_of_hundred_px.get_rect()
  r_o = surface_of_one_px.get_rect()


  from random import choice
  colors = ['white', 'blue']
  clock = pygame.time.Clock()


  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:    # check for keyboard inputs
        if event.key == pygame.K_RIGHT:
          r_h.x+=10
        if event.key == pygame.K_LEFT:
          r_h.x-=10                       # arrow inputs (moves red rectangle)
        if event.key == pygame.K_UP:
          r_h.y-=10
        if event.key == pygame.K_DOWN: 
          r_h.y+=10
        if event.key == pygame.K_d:
          if r_o.x < r_h.width-1:
            r_o.x+=1
        if event.key == pygame.K_a:
          if r_o.x > 0:
            r_o.x-=1                        # w,a,s,d inputs (moves tiny rectangle)
        if event.key == pygame.K_w:
          if r_o.y > 0:
            r_o.y-=1                        # the extra if statements are to keep the tiny rectangle
        if event.key == pygame.K_s:         #           always inside the red rectangle
          if r_o.y < r_h.height-1:
            r_o.y+=1

    
    screen.fill('white')
    area_of_hundred_px.fill('red')
    surface_of_one_px.fill(choice(colors))
    area_of_hundred_px.blit(surface_of_one_px,r_o) # Notice how we can blit surfaces on any surface,
                                                # we are not using screen.blit this time, but we
                                                # are using area_of_hundred_px.blit, and we are displaying
                                                # a blinking light at (x=0,y=0) wich is
                                                # the first pixel of area_of_hundred_px this time.
                                                # Also, notice how this position is independent
                                                # of the position of the red rectangle.
                                                #
                                                # If you would print r_h, if you move one time to the right,
                                                # you will get -> Rect(10, 0, 10, 10), being the parameters:
                                                # Rect(x,y,width,height) remember x,y is the topleft.
                                                #  
                                                # But r_o doesn't care how much you move your red rectangle
                                                # because r_o will always return -> Rect(0, 0, 1, 1)
                                                # unless that you move r_o directly.
                                                #
                                                # If you move r_o one time to the right, now you will get:
                                                # Rect(1, 0, 1, 1), wich means that you are on the second pixel
                                                # of your red rectangle.
    #print(r_h)
    #print(r_o) 
    screen.blit(area_of_hundred_px, r_h) # we blit our red surface, what contains another surface inside
    screen.blit(text, text_rect)
    clock.tick(30)
    pygame.display.flip()

  pygame.quit()



  # ╔═════════════════════════════════════════════════════════════════════════════════════════╗
  # ║  You completed this section you can close the program, and continue with the next one.  ║
  # ╠═════════════════════════════════════════════════════════════════════════════════════════╣



"""
|||||||||||||||||||||||||||
  HELPFUL RECT PROPERTIES 
|||||||||||||||||||||||||||
"""
if section3:
  # The properties of pygame Rects are:
  #   •bottom
  #   •bottomleft
  #   •bottomright
  #   •top
  #   •topleft
  #   •topright
  #   •center
  #   •centerx
  #   •centery
  #   •left
  #   •right
  #   •x
  #   •y
  #   •w 
  #   •h

  # This properties are diferent points in our rectangle,
  # being topleft the top left corner of our rectangle,
  # topright the top right corner, center, being the center of our rectangle, etc.
  time.sleep(1)
  pygame.init()
  screen = pygame.display.set_mode((800,400))
  screen_rect = screen.get_rect()
  pygame.display.set_caption('Surfaces and Rectangles')
  font = pygame.font.SysFont('Century Gothic',20)
  text = font.render('Press arrow keys to move',True,'black')
  text_rect = text.get_rect(center= screen_rect.center)

  #creating a bunch of surfaces and rects
  # you can see the full list of colors in
  pygame.colordict

  s= pygame.Surface((100,100)) 
  s.fill((255, 215, 0, 255))
  s_rect = s.get_rect() # does not define a position, so the default is going to be topleft = (0,0)

  s2 = pygame.Surface((50,50))
  s2.fill('brown')
  s2_rect = s2.get_rect(center = s_rect.center) # this line means: s2_rect.center = s_rect.center
                                                # in other words, the center point of s2_rect will be placed
                                                # on the center of s_rect.

  s3 = pygame.Surface((25,25))
  s3.fill('burlywood')
  s3_rect = s3.get_rect(center = (s2_rect.centerx-25, s2_rect.centery-25)) # the same is happening here.
                                                                          # but we need to subtract the size
                                                                          # of the surface in this case w=25,h=25

  s4 = pygame.Surface((12,12))
  s4.fill("lightgrey")
  s4_rect = s4.get_rect(center =(s3_rect.centerx-12, s3_rect.centery-12)) # put the center on the center and subtract


  s5 = pygame.Surface((60,20))
  s5.fill("lime")
  s5_rect = s5.get_rect(topleft = s_rect.bottomright) # the topleft of s5 will be placed at the bottomright of s

  s6 = pygame.Surface((80,80))
  s6.fill("greenyellow")
  s6_rect = s6.get_rect(topright = s5_rect.bottomleft)

  s7 = pygame.Surface((80,80))
  s7.fill('yellow')
  s7_rect = s7.get_rect(topleft= s6_rect.center)

  # try to create more surfaces yourself ‼
  # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓










  clock = pygame.time.Clock()
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    # if you click on a color, you can see the RGB values of the color you pressed
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        print(screen.get_at(event.pos))
    # using pygame.key.get_pressed() to detect a key that is being held down.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
      s_rect.x +=500*dt
    if keys[pygame.K_LEFT]:
      s_rect.x -=500*dt
    if keys[pygame.K_UP]:  # using get_pressed and delta time
      s_rect.y -=500*dt
    if keys[pygame.K_DOWN]:
      s_rect.y +=500*dt
    screen.fill((255,255,255))
    # this keeps a rectangle inside of another rectangle (avoids the player to exit the screen)
    s_rect.clamp_ip(screen_rect)
    # manually blitting everything
    s3.blit(s4, s4_rect) #s4 will be inside of s3
    s2.blit(s3, s3_rect) #s3 will be inside of s2
    s.blit(s2, s2_rect)  #s2 will be inside of s
    screen.blit(s, s_rect) #finally s will be inside of our screen surface
    screen.blit(s5, s5_rect)
    screen.blit(s6, s6_rect) 
    screen.blit(s7, s7_rect) 
    screen.blit(text, text_rect) 
    dt = clock.tick(60)/1000
    pygame.display.update()



  # ╔═════════════════════════════════════════════════════════════════════════════════════════╗
  # ║                             You completed all sections ♦                                ║
  # ╠═════════════════════════════════════════════════════════════════════════════════════════╣
    

  # Now you know:
  #  • How to manually create surfaces or load them, change their color and display them. 
  #  • Add Surfaces/Rectangles, once at a time with keydown events, or by using get_pressed.
  #  • Properties of Rects and how they work.
  #  • Centralize Surfaces/Rectangles
    
  # Some methods you saw:
  # • surface.fill()
  # • surface.blit()
  # • surface.get_rect()
  # • rect.clamp_ip()
  # • pygame.key.get_pressed()
  # • pygame.font.SysFont()
  # • font.render()
  # • pygame.time.Clock()
  # • clock.tick()
    

  # If you want to repeat a section, you can disable the sections you are not interested in
  #                     by setting the section to False (line 13).
