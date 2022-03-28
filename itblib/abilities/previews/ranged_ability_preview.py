"""Contains the RangedAttackAbilityPreview class."""

from typing import TYPE_CHECKING

import pygame
from pygame.constants import BLEND_RGB_ADD, BLEND_RGB_MULT

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.abilities.previews.abilitiy_preview_base import AbilityPreviewBase
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from itblib.globals.math_helpers import get_parabola_full
from itblib.net.NetEvents import NetEvents
from itblib.ui.widgets.ui_widget import TextBox
from itblib.Vec import add, smult, sub

if TYPE_CHECKING:
    from typing import Callable, Generator

class RangedAttackAbilityPreview(AbilityPreviewBase):
    """Creates previews for attacks with an arcing projectile."""

    def __init__(self, ability:AbilityBase) -> None:
        super().__init__(ability)
        owner = ability.get_owner()
        self.damagetextbox = TextBox(text='70', fontsize=16, bgcolor=(0,0,0,100), linewidth=16)
        self._bgbox = TextBox(text='  ', fontsize=16, textcolor=(0,100,0,100), bgcolor=(100,100,100,100), linewidth=18)
        self._start = owner.pos
        self._color:"tuple[int,int,int]" = NetEvents.session._players[owner.ownerid].color if NetEvents.session else [255,0,255]

    #pylint: disable=missing-function-docstring
    def get_blit_func(self, transform_func: "Callable[[tuple[int,int]], tuple[int,int]]") -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        aoe = list(self._ability.area_of_effect)
        if self._ability.primed and len(aoe) == 1:
            end = transform_func(aoe[0][0])
            p_1 = add(transform_func(self._start), smult(.5, STANDARD_UNIT_SIZE))
            p_2 = add(end, smult(.5, STANDARD_UNIT_SIZE))
            flip = p_1[0] > p_2[0]
            screen_left = p_1 if not flip else p_2
            screen_right = p_2 if not flip else p_1
            size = (screen_right[0] - screen_left[0] + 20, abs(screen_right[1] - screen_left[1]) + 100 + 10)
            topleft = (screen_left[0]-10, min(screen_left[1], screen_right[1]) - 50)
            surf = pygame.Surface(size).convert_alpha()
            surf.fill(0)
            left = sub(screen_left, topleft)
            right = sub(screen_right, topleft)
            p_peak = (surf.get_width() / 2, 0)
            target = left if flip else right
            pygame.draw.circle(surf, self._color, target, 10)
            if abs(left[0] - right[0]) <= 1e-10:
                pygame.draw.line(surf, self._color, (left[0], max([right[1], left[1]])), p_peak, 2)
            else:
                _draw_parabola(surf, self._color, p_peak, left, right)
            surf.blit(self._bgbox.image, sub(target, smult(.5,self._bgbox.get_size())), special_flags=BLEND_RGB_MULT)
            surf.blit(self.damagetextbox.image, sub(target, smult(.5,self.damagetextbox.get_size())), special_flags=BLEND_RGB_ADD)
            yield surf, pygame.Rect( add(topleft,(0,-10)), (size[0],size[1]/2) ), surf.get_rect()
        else:
            yield from self._get_simple_preview_gen(transform_func)
        return

def _draw_parabola(surface, color, peak, p1, p2):
    assert p1[0] < peak[0] < p2[0]
    parabola = get_parabola_full(peak, p1, p2)
    prev_point = p1
    step = 1
    for x in range(int(p1[0]), int(p2[0]), step):
        next_point = (x, parabola(x))
        pygame.draw.line(surface, color, prev_point, next_point, 2)
        prev_point = next_point
    