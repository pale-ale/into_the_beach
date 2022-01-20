from math import atan2, degrees, pi
from typing import Callable, Generator

import pygame
from itblib.abilities.AbilityBase import AbilityBase
from itblib.abilities.previews.AbilityPreviewBase import AbilityPreviewBase
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from itblib.net.NetEvents import NetEvents
from itblib.ui.TextBox import TextBox
from itblib.Vec import add, deg_to_coord, mult2, smult, sub


class ConeAttackAbilityPreview(AbilityPreviewBase):
    """Creates previews for attacks with a conical shape."""

    def __init__(self, ability:AbilityBase) -> None:
        super().__init__(ability)
        owner = ability.get_owner()
        self.damagetextbox = TextBox(text='7', fontsize=15, bgcolor=(0,0,0,100))
        self.cone_angle:float = pi/4
        self.cone_center_angle:float = pi/2
        self.cone_length:int = 100
        self._bgbox = TextBox(text='  ', fontsize=15, textcolor=(0,100,0,100), bgcolor=(0,100,150,100))
        if owner and NetEvents.session:
            self._color:"tuple[int,int,int]" = NetEvents.session._players[owner.ownerid].color
            self._start = owner.pos
        else:
            self._color = (100,100,100)
            self._start = None

    def get_blit_func(self, transform_func: Callable[["tuple[int,int]"], "tuple[int,int]"]) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        p_1 = add(transform_func(self._start), smult(.5, STANDARD_UNIT_SIZE), (0,7))
        size = (2*self.cone_length, 1.5*self.cone_length)
        topleft = sub(p_1, smult(.5, size))
        surf = pygame.Surface(size).convert_alpha()
        surf.fill(0)
        _draw_cone(surf, self._color, self.cone_angle, self.cone_center_angle, self.cone_length, smult(.5,size))
        yield surf, pygame.Rect( add(topleft,(0,-10)), (size[0],size[1]/2) ), surf.get_rect()

def _draw_cone(surface, color, cone_angle, cone_center_angle, cone_len, center):
    langle, rangle = cone_center_angle - cone_angle*.75, cone_center_angle + cone_angle*.75
    arc_left = add(center, mult2((1,.75), smult(cone_len, deg_to_coord(langle))))
    arc_right = add(center, mult2((1,.75), smult(cone_len, deg_to_coord(rangle))))
    arc_rect2 = pygame.Rect((0,0), (2*cone_len, 1.5*cone_len))
    pygame.draw.line(surface, color, arc_left, center)
    pygame.draw.line(surface, color, arc_right, center)
    pygame.draw.arc(surface, color, arc_rect2, -rangle, -langle)

def _get_angle(p1, p2):
    """@return: angle between p1 and p2 and screen x-axis"""
    dx = (p2[0]-p1[0])
    dy = (p2[1]-p1[1])
    return dx, dy, degrees( atan2( dy , dx ))
