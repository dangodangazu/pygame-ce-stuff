# newbie program example of how to use a room system in pygame

import pygame
from sys import exit as sys_exit

pygame.init()

screen_w = pygame.display.get_desktop_sizes()[0][0]
screen_h = pygame.display.get_desktop_sizes()[0][1]

screen = pygame.display.set_mode((screen_w, screen_h))
screen_rect = screen.get_rect()

#creating some instructions
font = font = pygame.font.SysFont('Arial', 25)
text = font.render('Press right or left to move, press ESC to exit.',True, 'white')
text2 = font.render('YOU WON :D',True, 'white')
text2_rect = text2.get_rect(center= (screen_w//2, screen_h//2))

#function to display some texts (text that changes such as fps, or in this case current_room)
def debug(info, x=10, y=10):
    font = pygame.font.SysFont('Arial', 25)
    debug_surf = font.render(str(info),True, "white")
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    screen.blit(debug_surf, debug_rect)

#creating the player
player = pygame.Surface((64,64))
player.fill('orange')
player_rect = player.get_rect(topleft = (screen_w//2, screen_h//2))
player_speed = 800
#creating the rooms
room1 = pygame.Surface((screen_w, screen_h))
room1.fill((100,100,100))
room2 = pygame.Surface((screen_w, screen_h))
room2.fill((80,80,80))
room3 = pygame.Surface((screen_w, screen_h))
room3.fill((60, 60, 60))
#creating a door
door = pygame.Surface((10,64))
door.fill('brown')
door_rect = door.get_rect(topright= (screen_w, screen_h//2))
#creating the door that is on the left
exit_door = pygame.Surface((10,64))
exit_door.fill('brown')
exit_door_rect = door.get_rect(topleft= (0, screen_h//2))


clock = pygame.time.Clock()


class RoomHandler:
  def __init__(self) -> None:
    self.current_room = 0
    self.rooms = [room1, room2, room3]


  def move_to_next_room(self, player_rect):
    if player_rect.colliderect(door_rect): #Rect method that checks collision between 2 rects
      
      self.current_room+=1 #increase the index
      player_rect.left = +15  #teleport the player  

  def move_to_past_room(self, player_rect):
    if self.current_room >0:
      if player_rect.colliderect(exit_door_rect): 
        self.current_room-=1 #decrease the index
        player_rect.right = screen_w-15  #teleport the player at the end of the screen minus some amount so it doesn't collide again


room_handler = RoomHandler()


while True:
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      pygame.quit()
      sys_exit()
    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
      pygame.quit()
      sys_exit()
  
  dt = clock.tick(60)/1000

  #Movement
  keys=pygame.key.get_pressed()
  if keys[pygame.K_RIGHT]:
    player_rect.x += player_speed*dt
    player_rect.clamp_ip(screen_rect)
  elif keys[pygame.K_LEFT]:
    player_rect.x -= player_speed*dt
    player_rect.clamp_ip(screen_rect)

  #blitting everything
  screen.fill((40,40,40))
  room_handler.move_to_next_room(player_rect) #not the best to check for a whole rect, we could check for a point
  room_handler.move_to_past_room(player_rect) # the same here but for the door on the left
  if room_handler.current_room <3:
    screen.blit(room_handler.rooms[room_handler.current_room], (0,0))
    screen.blit(player, player_rect)
    screen.blit(door, door_rect)
    screen.blit(exit_door, exit_door_rect)

  else:
    screen.blit(text2, text2_rect)
  screen.blit(text, (0,0))
  debug(f'ROOM: {room_handler.current_room}', 0, 50)
  pygame.display.update()

