"""Contains the ConeAttackAbilityPreview"""

from typing import TYPE_CHECKING

import pygame
from itblib.abilities.base_abilities.cone_ability_base import ConeAbilityBase
from itblib.abilities.previews.abilitiy_preview_base import AbilityPreviewBase
from itblib.globals.Constants import STANDARD_TILE_SIZE, STANDARD_UNIT_SIZE
from itblib.net.NetEvents import NetEvents
from itblib.ui.widgets.TextBox import TextBox
from itblib.Vec import add, deg_to_coord, mult2, smult, sub

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
    def get_blit_func(self, transform_func: "Callable[[tuple[int,int]], tuple[int,int]]") -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        cone_length = self._ability.cone_len_tiles * STANDARD_TILE_SIZE[0]
        if self._ability.selected or self._ability.primed:
            owner = self._ability.get_owner()
            if owner:
                p_1 = add(transform_func(self._ability.get_owner().pos), smult(.5, STANDARD_UNIT_SIZE), (0,7))
            size = (2*cone_length, 2*cone_length*self.yscale)
            topleft = sub(p_1, smult(.5, size))
            surf = pygame.Surface(size).convert_alpha()
            surf.fill(0)
            self._draw_cone(surf, cone_length, smult(.5,size), self.yscale)
            yield from self._get_simple_preview_gen(transform_func)
            yield surf, pygame.Rect(add(topleft,(0,-10)), (size[0],size[1])), surf.get_rect()

    def _draw_cone(self, surface:pygame.Surface, cone_len, center, yscale):
        langle = self._ability.cone_direction + .5*self._ability.cone_spread_angle
        rangle = self._ability.cone_direction - .5*self._ability.cone_spread_angle
        arc_left  = add(center, mult2((1,-yscale), smult(cone_len, deg_to_coord(langle))))
        arc_right = add(center, mult2((1,-yscale), smult(cone_len, deg_to_coord(rangle))))
        arc_rect2 = pygame.Rect((0,0), (2*cone_len, 2*cone_len*yscale))
        pygame.draw.line(surface, self._color, arc_left, center)
        pygame.draw.line(surface, self._color, arc_right, center)
        pygame.draw.arc(surface, self._color, arc_rect2, rangle, langle)
