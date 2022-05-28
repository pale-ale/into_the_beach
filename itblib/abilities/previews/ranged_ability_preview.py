"""Contains the RangedAttackAbilityPreview class."""

from typing import TYPE_CHECKING

import pygame
from pygame.constants import BLEND_RGB_ADD, BLEND_RGB_MULT
from itblib.Vec import IVector2

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.abilities.previews.abilitiy_preview_base import AbilityPreviewBase
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from itblib.globals.math_helpers import get_parabola_full
from itblib.net.NetEvents import NetEvents
from itblib.ui.widgets.ui_widget import TextBox

if TYPE_CHECKING:
    from typing import Callable, Generator
    from pygame import Surface, Rect

class RangedAttackAbilityPreview(AbilityPreviewBase):
    """Creates previews for attacks with an arcing projectile."""

    def __init__(self, ability:AbilityBase) -> None:
        super().__init__(ability)
        owner = ability.get_owner()
        self.damagetextbox = TextBox(text='70', fontsize=16, bgcolor=(0,0,0,100), linewidth=16)
        self._bgbox = TextBox(text='  ', fontsize=16, textcolor=(0,100,0,100), bgcolor=(100,100,100,100), linewidth=18)
        self._start = owner.position
        self._color:"tuple[int,int,int]" = NetEvents.session._players[owner.ownerid].color if NetEvents.session else [255,0,255]

    #pylint: disable=missing-function-docstring
    def get_blit_func(self, transform_func: "Callable[[IVector2], IVector2]") -> "Generator[Surface, Rect, Rect]":
        aoe = list(self._ability.area_of_effect)
        if self._ability.primed and len(aoe) == 1:
            end = transform_func(aoe[0][0])
            p_1 = transform_func(self._start) + IVector2(STANDARD_UNIT_SIZE) * .5
            p_2 = end + IVector2(STANDARD_UNIT_SIZE) * .5
            flip = p_1.x > p_2.x
            screen_left = p_1 if not flip else p_2
            screen_right = p_2 if not flip else p_1
            size = (screen_right.x - screen_left.x + 20, abs(screen_right.y - screen_left.y) + 100 + 10)
            topleft = IVector2(screen_left.x - 10, min(screen_left.y, screen_right.y) - 50)
            surf = pygame.Surface(size).convert_alpha()
            surf.fill(0)
            left = screen_left - topleft
            right = screen_right - topleft
            p_peak = IVector2(int(surf.get_width() / 2), 0)
            target = left if flip else right
            pygame.draw.circle(surf, self._color, target.c, 10)
            if abs(left.x - right.x) <= 1e-10:
                pygame.draw.line(surf, self._color, (left.x, max(right.y, left.y)), p_peak.c, 2)
            else:
                _draw_parabola(surf, self._color, p_peak, left, right)
            bgpos = target - IVector2(self._bgbox.get_size()) * .5
            dmgpos = target - IVector2(self.damagetextbox.get_size()) * .5
            surf.blit(self._bgbox.image,        bgpos.c,  special_flags=BLEND_RGB_MULT)
            surf.blit(self.damagetextbox.image, dmgpos.c, special_flags=BLEND_RGB_ADD)
            yield surf, pygame.Rect((topleft - (0,+10)).c, (size[0],size[1]/2) ), surf.get_rect()
        else:
            yield from self._get_simple_preview_gen(transform_func)
        return

def _draw_parabola(surface, color, peak:IVector2, p1:IVector2, p2:IVector2):
    assert p1.x < peak.x < p2.x
    parabola = get_parabola_full(peak.c, p1.c, p2.c)
    prev_point = p1
    step = 1
    for x in range(int(p1.x), int(p2.x), step):
        next_point = IVector2(x, int(parabola(x)))
        pygame.draw.line(surface, color, prev_point.c, next_point.c, 2)
        prev_point = next_point
    