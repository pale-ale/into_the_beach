import math
from itblib.abilities.AbilityBase import AbilityBase
from itblib.abilities.previews.AbilityPreviewBase import AbilityPreviewBase
from itblib.globals.Constants import STANDARD_UNIT_SIZE
import pygame
from itblib.net.NetEvents import NetEvents
from typing import Callable, Generator
from itblib.Vec import add, smult, sub

class RangedAttackAbilityPreview(AbilityPreviewBase):
    """Creates previews for a unit based on it's abilities and their targets."""

    def __init__(self, ability:AbilityBase) -> None:
        super().__init__(ability)
        owner = ability.get_owner()
        if owner and NetEvents.session:
            self._color:"tuple[int,int,int]" = NetEvents.session._players[owner.ownerid].color
            self._start = owner.pos
        else:
            self._color = (100,100,100)
            self._start = None

    def get_blit_func(self, transform_func: Callable[["tuple[int,int]"], "tuple[int,int]"]) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        aoe = list(self._ability.area_of_effect)
        if self._ability.primed and len(aoe) == 1:
            end = transform_func(aoe[0][0])
            p_1 = add(transform_func(self._start), smult(.5, STANDARD_UNIT_SIZE))
            p_2 = add(end, smult(.5, STANDARD_UNIT_SIZE))
            size = (abs(p_2[0] - p_1[0])+20, abs(p_2[1] - p_1[1]) + 100 + 10)
            topleft = (min(p_1[0], p_2[0])-10, min(p_1[1], p_2[1]) - 50)
            surf = pygame.Surface(size).convert_alpha()
            surf.fill(0)
            p_1 = sub(p_1, topleft)
            p_2 = sub(p_2, topleft)
            p_peak = (surf.get_width() / 2, 0)
            pygame.draw.circle(surf, self._color, p_2, 10)
            if abs(p_2[0] - p_1[0]) <= 1e-10:
                pygame.draw.line(surf, self._color, (p_1[0], max([p_1[1], p_2[1]])), p_peak, 2)
            else:
                _draw_parabola(surf, self._color, p_peak, p_1, p_2)
            yield surf, pygame.Rect( add(topleft,(0,-10)), (size[0],size[1]/2) ), surf.get_rect()
        else:
            yield from self._get_simple_preview_gen(transform_func)
        return

def _get_parabola(point, peak):
    t_point = (point[0] - peak[0], point[1] - peak[1])
    a = t_point[1]/t_point[0]**2 if t_point[0] != 0 else None
    return lambda x: a*x**2

def _draw_parabola(surface, color, peak, p1, p2):
    for point in (p1,p2):
        p = _get_parabola(point, peak)
        prev_point = (peak)
        step = int(math.copysign(2, point[0]- peak[0]))
        for x in range(int(peak[0]+step), int(point[0]+step), step):
            next_point = (x, p(x-peak[0])+peak[1])
            pygame.draw.line(surface, color, prev_point, next_point, 2)
            prev_point = next_point
    