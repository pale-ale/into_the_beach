import random

import pygame
from itblib.globals.Enums import RIVER
from itblib.gridelements.Effects import EffectBase
from itblib.gridelements.GridElementUI import GridElementUI
from itblib.ui.IDisplayable import IDisplayable
from itblib.Vec import scalar_mult


class EffectBaseUI(GridElementUI, IDisplayable):
    def __init__(self, effect:EffectBase, global_transform:pygame.Rect, framespeed:float=.5, autoplay=True):  
        super().__init__(parentelement=effect, global_transform=global_transform, direction=None, framespeed=framespeed)
        if autoplay:
            self.looping = True
            self.start()
    
    def get_display_description(self) -> str:
        return "Effect description"

    def get_display_name(self) -> str:
        return "Effect name"

class EffectRiverUI(EffectBaseUI):
    def update(self, delta_time:float):
        grid = self._parentelement.grid
        pos = self._parentelement.pos
        neighborposs = grid.get_ordinal_neighbors(pos)
        riverposs = []
        for test_pos in neighborposs: 
            for effect in grid.get_worldeffects(test_pos):
                if type(effect).__name__ == "EffectRiver":
                    riverposs.append(test_pos)
        if len(riverposs) == 0:
            imageid = 4
        elif len(riverposs) == 1:
            imageid = 5
        elif len(riverposs) == 2:
            prev, next = riverposs
            prevdelta = (pos[0] - prev[0], pos[1] - prev[1])
            nextdelta = (next[0] - pos[0], next[1] - pos[1])
            imageid = RIVER[(*nextdelta, *prevdelta)]
        else:
            print("EffectRiverUI: Weird riverposs:", riverposs)
            return
        self.set_frame(imageid)
    
    def get_display_name(self) -> str:
        return "River"

class EffectFireUI(EffectBaseUI):
    def __init__(self, effect: EffectBase, global_transform: pygame.Rect, framespeed: float = 0.5):
        super().__init__(effect, global_transform, framespeed=framespeed, autoplay=False)
        self.im = pygame.Surface((64,64)).convert_alpha()
        self.im.fill(100)
        self.desired_particles = 40
        self.fire_left = 16
        self.fire_right = 48
        self.max_particle_lifetime = 5
        self.particle_xs        = [None] * self.desired_particles
        self.particle_ys        = [None] * self.desired_particles
        self.particle_colors    = [None] * self.desired_particles
        self.particle_lifetimes = [self.max_particle_lifetime+1] * self.desired_particles
    
    def update(self, delta_time: float):
        for p in range(self.desired_particles):
            self.particle_lifetimes[p] += delta_time
            if self.particle_lifetimes[p] > self.max_particle_lifetime:
                self.particle_lifetimes[p] = random.random()*4
                self.particle_colors[p] = (255, random.randint(0,150), 0)
                x = random.randint(self.fire_left,self.fire_right)
                #x = self.fire_left
                ydiv = 16 - abs((self.fire_left + self.fire_right)/2 - x)
                self.particle_xs[p] = x
                self.particle_ys[p] = 28 - random.randint(-ydiv, ydiv)
                continue
            self.particle_xs[p] += random.randint(-1,1) if random.random() < delta_time*3 else 0
            self.particle_ys[p] -= 1 if random.random() < delta_time*4 else 0
        self.im.fill(100)
        for p in range(self.desired_particles):
            self.im.fill(
                scalar_mult(
                    min(1,((self.max_particle_lifetime - self.particle_lifetimes[p])/self.max_particle_lifetime)*2.5), 
                    self.particle_colors[p]), 
                (self.particle_xs[p], self.particle_ys[p], 3, 3))

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.im, self.global_transform, self.im.get_rect())

