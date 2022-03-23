"""Contains various animations."""

from typing import TYPE_CHECKING
from itblib.globals.Colors import DARK_GRAY
from itblib.ui.animations.MultiSprite import MultiSprite
from itblib.ui.particles import TrailParticleSpawner
import pygame

if TYPE_CHECKING:
    from typing import Generator, Callable

class ProjectileAnimation(MultiSprite):
    def __init__(self, playtime:float, pos_func:"Callable[[float],tuple[int,int]]"):
        self._particles_spawner = TrailParticleSpawner()
        self._bullet_texture = pygame.Surface((7,7)).convert_alpha()
        self._bullet_texture.fill((0))
        self._pos = (0,0)
        self._pos_func = pos_func
        self._playtime = playtime
        pygame.draw.circle(self._bullet_texture, DARK_GRAY, (3,3), 3)
        super().__init__([], playing=True)
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self._bullet_texture, pygame.Rect(self._pos, (7,7)), self._bullet_texture.get_rect())
        yield from self._particles_spawner.get_blits()
    
    def update(self, delta_time: float):
        self.animtime += delta_time
        if self.animtime >= self._playtime:
            self.playing = False
        if self.playing:
            self._pos = self._pos_func(self.animtime)
            self._particles_spawner.position = (self._pos[0] - 25, self._pos[1]-22)
            self._particles_spawner.update(delta_time)
        return