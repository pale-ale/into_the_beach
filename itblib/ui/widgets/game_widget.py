"""A collection of Widgets displayed in the world."""

from typing import TYPE_CHECKING
import pygame
from itblib.damage_receiver import DamageReceiver
from itblib.globals.Colors import HP_ABSENT, HP_BORDER, HP_PADDING, HP_PRESENT
from itblib.ui.widgets.ui_widget import Widget
from itblib.globals.Constants import STANDARD_UNIT_SIZE

from itblib.Vec import add

if TYPE_CHECKING:
    from typing import Generator
    from itblib.gridelements.UnitsUI import UnitBaseUI

class HealthBar(Widget):
    """A Widget used to display the amount health and max health a DamageReceiver possesses."""
    def __init__(self, target:DamageReceiver):
        super().__init__()
        self._target = target
        self._min_hp_width = 4
        self._max_hp_width = 8
        self._hp_height = 5
        self._outer_padding = 1
        self._inner_padding = 1
        self._hp_width = max(self._min_hp_width, self._max_hp_width - self._target._max_hitpoints)
        self._width_per_hp = (self._hp_width+self._inner_padding)
        self._inner_width = self._width_per_hp * self._target._max_hitpoints + self._inner_padding
        self.width = self._inner_width + 2*self._outer_padding
        self._inner_height = self._hp_height + 2*self._inner_padding
        self.height = self._inner_height + 2*self._outer_padding
        self.image = pygame.Surface((self.width, self.height))
        self._target.hp_update_callback = self.on_update_hp

    def _draw_bg(self):
        self.image.fill(HP_PADDING)
        bg_rect = (self._outer_padding, self._outer_padding, self._inner_width, self._inner_height)
        self.image.fill(HP_BORDER, bg_rect)

    def _draw_bars(self):
        hp_size = (self._hp_width, self._hp_height)
        for i in range(self._target._max_hitpoints):
            hp_pos = (self._inner_padding + i*(self._width_per_hp), self._inner_padding)
            self.image.fill(
                HP_PRESENT if i < self._target.hitpoints else HP_ABSENT,
                (
                    add(hp_pos, (self._outer_padding, self._outer_padding)),
                    hp_size
                )
            )

    def on_update_hp(self, new_hp:int):
        self._draw_bg()
        self._draw_bars()


class OwnerColorRhombus(Widget):
    """A Widget used to display a rhombus around a unit, using the owner's coloring."""
    def __init__(self, playercolor:tuple[int,int,int,int]) -> None:
        super().__init__()
        self._unit = None
        self._player_color = playercolor
        x = 48
        y = 32
        self._unit_owner_square_size = (x,y)
        self._unit_owner_square_corners = [
            (int(x/2+.5),            2),
            (x-3        ,int(y/2-.5)+1),
            (x-3        ,int(y/2+.5)+1),
            (int(x/2+.5),          y-1),
            (int(x/2-.5),          y-1),
            (          2,int(y/2+.5)+1),
            (          2,int(y/2-.5)+1),
            (int(x/2-.5),            2)
        ]
        self.image = pygame.Surface(self._unit_owner_square_size).convert_alpha()
        self.image.fill(0)
        self._draw_lines()
        self.position = ((STANDARD_UNIT_SIZE[0]-x)/2,(STANDARD_UNIT_SIZE[1]-y)-8)

    def attach_to_unit(self, unit:"UnitBaseUI"):
        self._unit = unit
        self.parent = unit

    def _draw_lines(self):
        pygame.draw.lines(
            self.image,
            self._player_color,
            True,
            self._unit_owner_square_corners,
            1
        )
