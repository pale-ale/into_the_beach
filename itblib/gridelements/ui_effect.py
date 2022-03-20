"""
A Collection of EffectUIs, used as a screen representation of WorldEffects and StatusEffects.
"""

import math
import random
from typing import TYPE_CHECKING

import pygame
from itblib.globals.Colors import TEXTURE_MISSING
from itblib.globals.Enums import RIVER
from itblib.gridelements.GridElementUI import GridElementUI
from itblib.gridelements.world_effects import WorldEffectBase
from itblib.ui.IDisplayable import IDisplayable
from itblib.ui.TextureManager import Textures

if TYPE_CHECKING:
    from typing import Generator


class EffectBaseUI(GridElementUI, IDisplayable):
    """Base class of the UI Effects, displaying World/StatusEffects."""
    def __init__(self, effect:WorldEffectBase, framespeed:float=.2, autoplay=True):
        super().__init__(parentelement=effect, direction=None, framespeed=framespeed)
        if autoplay:
            self.looping = False
            self.start()

    def get_display_description(self) -> str:
        return self._parentelement.get_display_description()

    def get_display_name(self) -> str:
        return self._parentelement.get_display_name()

    def get_icon(self) -> pygame.Surface:
        icon = pygame.Surface((16,16))
        icon.fill(TEXTURE_MISSING)
        return icon


class EffectRiverUI(EffectBaseUI):
    """Displays a river. Uses proximity texturing to connect to neighbours."""
    def update(self, delta_time:float):
        """Updates neighbors every tick."""
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
    """Displays fire."""
    def __init__(self, effect: WorldEffectBase, framespeed: float = 0.5):
        super().__init__(effect, framespeed=framespeed, autoplay=False)
        self.particle_space = pygame.Surface((64,64)).convert_alpha()
        self.particle_space.fill(0)
        self.desired_particles = 40
        self.fire_left = 16
        self.fire_right = 48
        self.max_particle_lifetime = 5
        self.particle_xs        = [None] * self.desired_particles
        self.particle_ys        = [None] * self.desired_particles
        self.particle_colors    = [None] * self.desired_particles
        self.particle_lifetimes = [self.max_particle_lifetime+1] * self.desired_particles

    def update(self, delta_time: float):
        """Update the fire particles."""
        self.particle_space.fill(0)
        for particle_index in range(self.desired_particles):
            self.particle_lifetimes[particle_index] += delta_time
            if self.particle_lifetimes[particle_index] > self.max_particle_lifetime:
                self.particle_lifetimes[particle_index] = random.random()*4
                x_pos = random.randint(self.fire_left,self.fire_right)
                ydiv = 16 - abs((self.fire_left + self.fire_right)/2 - x_pos)
                self.particle_xs[particle_index] = x_pos
                self.particle_ys[particle_index] = 28 - random.randint(-ydiv, ydiv)
                continue
            if random.random() < delta_time*3:
                self.particle_xs[particle_index] += (random.randint(-1,1)+random.randint(0,2))
            self.particle_ys[particle_index] -= 1 if random.random() < delta_time*4 else 0
        for particle_index in range(self.desired_particles):
            self.particle_space.fill(
                EffectFireUI._get_color(
                    self.particle_lifetimes[particle_index]/self.max_particle_lifetime
                ),
                (self.particle_xs[particle_index], self.particle_ys[particle_index], 3, 3)
            )

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        particle_rect = pygame.Rect(self.tfc.get_position(), self.particle_space.get_size())
        yield (self.particle_space, particle_rect, self.particle_space.get_rect())

    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Ablaze")[0]

    @staticmethod
    def _get_color(lifetime_ratio:float) -> "tuple[int,int,int,int]":
        assert lifetime_ratio >= 0 and lifetime_ratio < 1
        gradients = [(255,255,000,255), (255,000,000,255), (100,0,0,255), (0,0,0,0)]
        gradient_dim = 4
        index_float = lifetime_ratio*(len(gradients)-1)
        start = int(index_float)
        end = math.ceil(index_float)
        g_1 = gradients[start]
        g_2 = gradients[end]
        t_l = start/(len(gradients)-1)
        t_s = (lifetime_ratio - t_l)*2
        interp = tuple([int(g_1[x]*(1.0-t_s) + g_2[x]*t_s) for x in range(gradient_dim)])
        return interp


class EffectMountainUI(EffectBaseUI):
    """Displays a mountain."""
    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Mountain")[0]


class EffectWheatUI(EffectBaseUI):
    """Displays a wheat field."""
    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Wheat")[0]

class EffectHealUI(EffectBaseUI):
    """Displays a heal."""
    def __init__(self, effect: WorldEffectBase, framespeed: float = 0.1, autoplay=True):
        super().__init__(effect, framespeed, autoplay)

class EffectStartingAreaUI(EffectBaseUI):
    """Displays the player's starting area."""
    def __init__(self, effect: WorldEffectBase, framespeed: float = 0.2, autoplay=False):
        super().__init__(effect, framespeed, autoplay)

    def get_display_name(self) -> str:
        return "Drop Zone"
