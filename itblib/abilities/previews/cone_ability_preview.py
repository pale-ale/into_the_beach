"""Contains the ConeAttackAbilityPreview"""

from typing import TYPE_CHECKING

import pygame
from itblib.abilities.base_abilities.cone_ability_base import ConeAbilityBase
from itblib.abilities.previews.abilitiy_preview_base import AbilityPreviewBase
from itblib.globals.Constants import STANDARD_TILE_SIZE, STANDARD_UNIT_SIZE
from itblib.net.NetEvents import NetEvents
from itblib.ui.widgets.ui_widget import TextBox
from itblib.Vec import IVector2, deg_to_coord
from pygame import Surface, Rect

if TYPE_CHECKING:
    from typing import Callable, Generator


class ConeAttackAbilityPreview(AbilityPreviewBase):
    """Creates previews for attacks with a conical shape."""

    def __init__(self, ability:ConeAbilityBase) -> None:
        super().__init__(ability)
        self._ability:ConeAbilityBase
        self.damagetextbox = TextBox(text='7', fontsize=15, bgcolor=(0,0,0,100))
        owner = ability.get_owner()
        self.yscale = 44/STANDARD_TILE_SIZE[0]
        self._color:"tuple[int,int,int]" = NetEvents.session._players[owner.ownerid].color if NetEvents.session else [255,0,255]

    #pylint: disable=missing-function-docstring
    def get_blit_func(self, transform_func: "Callable[[IVector2], IVector2]") -> "Generator[tuple[Surface, Rect, Rect]]":
        cone_length = self._ability.cone_len_tiles * STANDARD_TILE_SIZE[0]
        if self._ability.selected or self._ability.primed:
            owner = self._ability.get_owner()
            p_1 = transform_func(self._ability.get_owner().position) + IVector2(STANDARD_UNIT_SIZE) * .5 + IVector2(0,7)
            size = IVector2(int(2*cone_length), int(2*cone_length*self.yscale))
            topleft = p_1 - size * .5
            surf = pygame.Surface(size.c).convert_alpha()
            surf.fill(0)
            self._draw_cone(surf, cone_length, size * .5, self.yscale)
            yield from self._get_simple_preview_gen(transform_func)
            yield surf, pygame.Rect((topleft - (0,10)).c, size.c), surf.get_rect()

    def _draw_cone(self, surface:Surface, cone_len:float, center:IVector2, yscale:float):
        langle = self._ability.cone_direction + .5 * self._ability.cone_spread_angle
        rangle = self._ability.cone_direction - .5 * self._ability.cone_spread_angle
        l = cone_len * deg_to_coord(langle)
        l.y *= -yscale
        r = cone_len * deg_to_coord(rangle)
        r.y *= -yscale
        arc_left  = center + IVector2(int(l.x), int(l.y))
        arc_right = center + IVector2(int(r.x), int(r.y))
        arc_rect2 = pygame.Rect((0,0), (2 * cone_len, 2 * cone_len * yscale))
        pygame.draw.line(surface, self._color, arc_left.c, center.c)
        pygame.draw.line(surface, self._color, arc_right.c, center.c)
        pygame.draw.arc(surface, self._color, arc_rect2, rangle, langle)
