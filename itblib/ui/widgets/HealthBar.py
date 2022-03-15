import pygame
from itblib.damage_receiver import DamageReceiver
from itblib.globals.Colors import HP_ABSENT, HP_BORDER, HP_PADDING, HP_PRESENT
from itblib.ui.widgets.Widget import Widget
from itblib.Vec import add


class HealthBar(Widget):
    def __init__(self, target:DamageReceiver):
        super().__init__()
        self._target = target
        self._min_hp_width = 4
        self._max_hp_width = 8
        self._hp_height = 5
        self._outer_padding = 1
        self._inner_padding = 1
        self._hp_width = max(self._min_hp_width, self._max_hp_width - self._target._max_hitpoints)
        self._inner_width = (self._hp_width+self._inner_padding) * self._target._max_hitpoints + self._inner_padding
        self.width = self._inner_width + 2*self._outer_padding
        self._inner_height = self._hp_height + 2*self._inner_padding 
        self.height = self._inner_height + 2*self._outer_padding 
        self.image = pygame.Surface((self.width, self.height))
        self._target.set_hp_update_callback(self.on_update_hp)
    
    def _draw_bg(self):
        self.image.fill(HP_PADDING)
        self.image.fill(HP_BORDER, (self._outer_padding, self._outer_padding, self._inner_width, self._inner_height))
    
    def _draw_bars(self):
        hp_size = (self._hp_width, self._hp_height)
        for i in range(self._target._max_hitpoints):
            hp_pos = (self._inner_padding + i*(self._hp_width+self._inner_padding), self._inner_padding)
            self.image.fill(
                HP_PRESENT if i < self._target._hitpoints else HP_ABSENT, 
                (
                    add(hp_pos, (self._outer_padding, self._outer_padding)),
                    hp_size
                )
            )
    
    def on_update_hp(self, hp:int):
        self._draw_bg()
        self._draw_bars()
