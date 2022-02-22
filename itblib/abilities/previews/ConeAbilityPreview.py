from typing import Callable, Generator

import pygame
from itblib.abilities.baseAbilities.ConeAttackAbilityBase import \
    ConeAttackAbilityBase
from itblib.abilities.previews.AbilityPreviewBase import AbilityPreviewBase
from itblib.globals.Constants import STANDARD_TILE_SIZE, STANDARD_UNIT_SIZE
from itblib.net.NetEvents import NetEvents
from itblib.ui.TextBox import TextBox
from itblib.Vec import add, deg_to_coord, mult2, smult, sub


class ConeAttackAbilityPreview(AbilityPreviewBase):
    """Creates previews for attacks with a conical shape."""

    def __init__(self, ability:ConeAttackAbilityBase) -> None:
        super().__init__(ability)
        self._ability:ConeAttackAbilityBase
        self.damagetextbox = TextBox(text='7', fontsize=15, bgcolor=(0,0,0,100))
        self._bgbox = TextBox(text='  ', fontsize=15, textcolor=(0,100,0,100), bgcolor=(0,100,150,100))
        owner = ability.get_owner()
        self.yscale = 44/STANDARD_TILE_SIZE[0]
        self._color:"tuple[int,int,int]" = NetEvents.session._players[owner.ownerid].color if NetEvents.session else [255,0,255]

    def get_blit_func(self, transform_func: Callable[["tuple[int,int]"], "tuple[int,int]"]) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        cone_length = self._ability.cone_len_tiles * STANDARD_TILE_SIZE[0]
        if self._ability.selected or self._ability.primed:
            owner = self._ability.get_owner()
            if owner:
                p_1 = add(transform_func(self._ability.get_owner().pos), smult(.5, STANDARD_UNIT_SIZE), (0,7))
            size = (2*cone_length, 2*cone_length*self.yscale)
            topleft = sub(p_1, smult(.5, size))
            surf = pygame.Surface(size).convert_alpha()
            surf.fill(0)
            _draw_cone(surf, self._color, self._ability.cone_spread_angle, self._ability.cone_direction, cone_length, smult(.5,size), self.yscale)
            yield from self._get_simple_preview_gen(transform_func)
            yield surf, pygame.Rect(add(topleft,(0,-10)), (size[0],size[1])), surf.get_rect()

def _draw_cone(surface:pygame.Surface, color, cone_angle, cone_center_angle, cone_len, center, yscale):
    langle, rangle = cone_center_angle + .5*cone_angle, cone_center_angle - .5*cone_angle
    arc_left  = add(center, mult2((1,-yscale), smult(cone_len, deg_to_coord(langle))))
    arc_right = add(center, mult2((1,-yscale), smult(cone_len, deg_to_coord(rangle))))
    arc_rect2 = pygame.Rect((0,0), (2*cone_len, 2*cone_len*yscale))
    pygame.draw.line(surface, color, arc_left, center)
    pygame.draw.line(surface, color, arc_right, center)
    pygame.draw.arc(surface, color, arc_rect2, rangle, langle)
