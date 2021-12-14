from typing import Generator

import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.DamageReceiver import DamageReceiver
from itblib.globals.Colors import HP_ABSENT, HP_BORDER, HP_PADDING, HP_PRESENT
from itblib.ui.PerfSprite import PerfSprite
from itblib.Vec import add


class HealthBar(ComponentAcceptor, PerfSprite):
    def __init__(self, target:DamageReceiver):
        ComponentAcceptor.__init__(self)
        self.tfc = TransformComponent()
        self.tfc.attach_component(self)
        self.target = target
        self._min_hp_width = 4
        self._max_hp_width = 8
        self._hp_height = 5
        self.outer_padding = 1
        self.inner_padding = 1
        self._hp_width = max(self._min_hp_width, self._max_hp_width - self.target._max_hitpoints)
        self._inner_width = (self._hp_width+self.inner_padding) * self.target._max_hitpoints + self.inner_padding
        self.width = self._inner_width + 2*self.outer_padding
        self._inner_height = self._hp_height + 2*self.inner_padding 
        self.height = self._inner_height + 2*self.outer_padding 
        self.image = pygame.Surface((self.width, self.height))
        #self.set_hp(self.target._hitpoints)
        self.target.set_hp_update_callback(self.set_hp)
    
    def _draw_bg(self):
        self.image.fill(HP_PADDING)
        self.image.fill(HP_BORDER, (self.outer_padding, self.outer_padding, self._inner_width, self._inner_height))
    
    def _draw_bars(self):
        hp_size = (self._hp_width, self._hp_height)
        for i in range(self.target._max_hitpoints):
            hp_pos = (self.inner_padding + i*(self._hp_width+self.inner_padding), self.inner_padding)
            self.image.fill(
                HP_PRESENT if i < self.target._hitpoints else HP_ABSENT, 
                (
                    add(hp_pos, (self.outer_padding, self.outer_padding)),
                    hp_size
                )
            )
    
    def set_hp(self, hp:int):
        self._draw_bg()
        self._draw_bars()
    
    def update(self, delta_time: float) -> None:
        return super().update(delta_time)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        pos = add(self.tfc.get_position(), (-int(self.width/2), -int(self.height/2)))
        yield (self.image, pygame.Rect(*pos, self.width, self.height), pygame.Rect(0,0,self.width,self.height))
