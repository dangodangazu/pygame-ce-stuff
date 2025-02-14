# example of perfect pixel colision & DirtySprite usage
# to make this i took reference here -> https://github.com/pygame-community/pygame-ce/blob/main/examples/mask.py 

import pygame as pg
import random
import numpy as np
from time import time

pg.init()
screen = pg.display.set_mode(pg.display.get_desktop_sizes()[0])
screen_ = screen.get_rect()
bg = pg.Surface(screen.get_size())
bg.fill("burlywood")
clock = pg.time.Clock()
running = True

path = "assets/img/gato.png"
name = "gato"
amount = 25
sprites = pg.sprite.LayeredDirty()
SPD = {}

CYCLES = 10_000
fps_list = [0] * CYCLES
increment = 0

pg.mouse.set_visible(0)

def debbug_n_stop_n_cycles(increment, np, fps_list, CYCLES, clock, start_time):
    fps_list[increment] = clock.get_fps()
    increment += 1
    if increment >= CYCLES:
        print(f"FPS AVERAGE: {np.mean(fps_list)}")
        pg.quit()
        print("ELAPSED TIME:", time() - start_time)
        raise SystemExit()
    return fps_list, increment


def rip(obj, kwargs):
    return obj.image.get_frect(
        **{k: v for k, v in kwargs.items() if k in {
            "topleft", "midtop", "topright", "midleft", "center", "midright", "bottomleft", "midbottom", "bottomright", "x", "y"
        }}
    )


class DirtySprite(pg.sprite.DirtySprite):
    def __init__(self, name, path, **kwargs):
        super().__init__()
        self.image = pg.image.load(path).convert_alpha()
        num = random.randint(0,1)
        if num == 0:
            self.image = pg.transform.scale2x(self.image)
        self.rect = rip(self, kwargs)
        self.mask = pg.mask.from_surface(self.image)
        self.pos = pg.Vector2(self.rect.topleft)
        self.vel = pg.Vector2(random.uniform(-200, 200), random.uniform(-200, 200))
        self.dirty = 2

    def collide(self, other):
        offset = [int(x) for x in other.pos - self.pos]
        overlap = self.mask.overlap_area(other.mask, offset)
        if overlap == 0:
            return

        n_collisions = pg.Vector2(
            self.mask.overlap_area(other.mask, (offset[0] + 1, offset[1])) -
            self.mask.overlap_area(other.mask, (offset[0] - 1, offset[1])),
            self.mask.overlap_area(other.mask, (offset[0], offset[1] + 1)) -
            self.mask.overlap_area(other.mask, (offset[0], offset[1] - 1))
        )
        if n_collisions.x == 0 and n_collisions.y == 0:
            return

        delta_vel = other.vel - self.vel
        j = delta_vel * n_collisions / (2 * n_collisions * n_collisions)
        if j > 0:
            j *= 1.9
            self.vel += [n_collisions.x * j, n_collisions.y * j]
            other.vel += [-j * n_collisions.x, -j * n_collisions.y]

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.topleft = self.pos
        self.dirty = 1


def create_many(amount):
    for i in range(amount):
        sprite = DirtySprite(name + str(i), path, x=random.randint(0, screen_.w), y=random.randint(0, screen_.h))
        SPD[name + str(i)] = sprite
        sprites.add(sprite)


create_many(amount)
START_TIME = time()

while running:
    dt = clock.tick(0) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    
    sprite_list = list(SPD.values())
    for i, sprite in enumerate(sprite_list):
        for other in sprite_list[i + 1:]:
            sprite.collide(other)

        if sprite.pos.x < -sprite.rect.w:
            sprite.pos.x = screen_.w
        elif sprite.pos.x > screen_.w:
            sprite.pos.x = -sprite.rect.w
    
        if sprite.pos.y < -sprite.rect.h:
            sprite.pos.y = screen_.h
        elif sprite.pos.y > screen_.h:
            sprite.pos.y = -sprite.rect.h
    
    sprites.update(dt)
    pg.display.update(sprites.draw(screen, bg))
    fps_list, increment = debbug_n_stop_n_cycles(increment, np, fps_list, CYCLES, clock, START_TIME)

pg.quit()
