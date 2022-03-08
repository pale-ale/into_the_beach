import math
import random
from typing import Generator

import pygame
from itblib.globals.Colors import TEXTURE_MISSING
from itblib.globals.Enums import RIVER
from itblib.gridelements.Effects import EffectBase
from itblib.gridelements.GridElementUI import GridElementUI
from itblib.ui.IDisplayable import IDisplayable
from itblib.ui.TextureManager import Textures


class EffectBaseUI(GridElementUI, IDisplayable):
    def __init__(self, effect:EffectBase, framespeed:float=.2, autoplay=True):  
        super().__init__(parentelement=effect, direction=None, framespeed=framespeed)
        if autoplay:
            self.looping = False
            self.start()
    
    def get_display_description(self) -> str:
        return self._parentelement.get_display_description()

    def get_display_name(self) -> str:
        return self._parentelement.get_display_name()
    
    def get_icon(self) -> pygame.Surface:
        s = pygame.Surface((16,16))
        s.fill(TEXTURE_MISSING)
        return s


class EffectRiverUI(EffectBaseUI):
    def update(self, delta_time:float):
        grid = self._parentelement.grid
        pos = self._parentelement.pos
        neighborposs = grid.get_neighbors(pos)
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
        self.framenumber = imageid
    

class EffectFireUI(EffectBaseUI):
    def __init__(self, effect: EffectBase, framespeed: float = 0.5):
        super().__init__(effect, framespeed=framespeed, autoplay=False)
        self.im = pygame.Surface((64,64)).convert_alpha()
        self.im.fill(0)
        self.desired_particles = 40
        self.fire_left = 16
        self.fire_right = 48
        self.max_particle_lifetime = 5
        self.particle_xs        = [None] * self.desired_particles
        self.particle_ys        = [None] * self.desired_particles
        self.particle_colors    = [None] * self.desired_particles
        self.particle_lifetimes = [self.max_particle_lifetime+1] * self.desired_particles
    
    def update(self, delta_time: float):
        self.im.fill(0)
        for p in range(self.desired_particles):
            self.particle_lifetimes[p] += delta_time
            if self.particle_lifetimes[p] > self.max_particle_lifetime:
                self.particle_lifetimes[p] = random.random()*4
                x = random.randint(self.fire_left,self.fire_right)
                ydiv = 16 - abs((self.fire_left + self.fire_right)/2 - x)
                self.particle_xs[p] = x
                self.particle_ys[p] = 28 - random.randint(-ydiv, ydiv)
                continue
            self.particle_xs[p] += (random.randint(-1,1)+random.randint(0,2)) if random.random() < delta_time*3 else 0
            self.particle_ys[p] -= 1 if random.random() < delta_time*4 else 0
        for p in range(self.desired_particles):
            self.im.fill(
                EffectFireUI._get_color(self.particle_lifetimes[p]/self.max_particle_lifetime),
                (self.particle_xs[p], self.particle_ys[p], 3, 3))

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.im, pygame.Rect(self.tfc.get_position(), self.im.get_size()), self.im.get_rect())
    
    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Ablaze")[0]
    
    @staticmethod
    def _get_color(lifetime_ratio:float) -> "tuple[int,int,int,int]":
        assert lifetime_ratio >= 0 and lifetime_ratio < 1
        gradients = [(255,255,000,255), (255,000,000,255), (100,0,0,255), (0,0,0,0)]
        gradient_dim = 4
        index_float = lifetime_ratio*(len(gradients)-1)
        l = int(index_float)
        r = math.ceil(index_float)
        g1 = gradients[l]
        g2 = gradients[r]
        t_l = l/(len(gradients)-1)
        t_s = (lifetime_ratio - t_l)*2
        interp = tuple([int(g1[x]*(1.0-t_s) + g2[x]*t_s) for x in range(gradient_dim)])
        return (interp)


class EffectMountainUI(EffectBaseUI):
    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Mountain")[0]


class EffectWheatUI(EffectBaseUI):
    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Wheat")[0]

class EffectHealUI(EffectBaseUI):
    def __init__(self, effect: EffectBase, framespeed: float = 0.1, autoplay=True):
        super().__init__(effect, framespeed, autoplay)
    
    def update(self, delta_time: float):
        super().update(delta_time)
        
class EffectStartingAreaUI(EffectBaseUI):
    def __init__(self, effect: EffectBase, framespeed: float = 0.2, autoplay=False):
        super().__init__(effect, framespeed, autoplay)
    
    def get_display_name(self) -> str:
        return "Drop Zone"
