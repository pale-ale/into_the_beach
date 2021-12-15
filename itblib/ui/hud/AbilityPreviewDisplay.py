from itblib.abilities.AbilityBase import AbilityBase
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from itblib.net.NetEvents import NetEvents
from itblib.ui.GridUI import GridUI
from itblib.ui.PerfSprite import PerfSprite
import pygame
from typing import Generator
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.ui.TextureManager import Textures
from itblib.Vec import add, smult, sub

class AbilityPreviewDisplay(PerfSprite):
    """Creates previews for a unit based on it's abilities and their targets."""

    def __init__(self, gridui:GridUI) -> None:
        super().__init__()
        self.unit:"UnitBase|None" = None
        self._gridui = gridui

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        for ability in self.unit.ability_component._abilities:
            if ability:
                yield from self._get_ability_blits(self.unit, ability)
    
    def update(self, delta_time: float) -> None:
        pass

    def _get_ability_blits(self, unit:UnitBase, ability:AbilityBase) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        aoe = ability.area_of_effect
        for pos, preview_name in aoe:
            global_target_pos = self._gridui.transform_grid_screen(pos)
            global_unit_pos = self._gridui.transform_grid_screen(unit.pos)
            if preview_name.startswith("Special"):
                s,r = self._draw_special_preview(unit.pos, aoe, NetEvents.session._players[unit.ownerid].color)
                yield (s, r, pygame.Rect((0,0),s.get_size()))
                return
            else:    
                yield (
                        Textures.textures[preview_name][0], 
                        pygame.Rect(*global_target_pos,64,64), 
                        pygame.Rect(0,0,64,64)
                    )
    
    def _draw_special_preview(self, unit_pos, aoe:"tuple[tuple[int,int],str]", playercolor):
        p_1 = add(self._gridui.transform_grid_screen(unit_pos), smult(.5, STANDARD_UNIT_SIZE))
        p_2 = add(self._gridui.transform_grid_screen(list(aoe)[0][0]), smult(.5, STANDARD_UNIT_SIZE))
        size = (abs(p_2[0] - p_1[0])+20, abs(p_2[1] - p_1[1]) + 100 + 10)
        topleft = (min(p_1[0], p_2[0])-10, min(p_1[1], p_2[1]) - 100)
        surf = pygame.Surface(size).convert_alpha()
        surf.fill(0)
        p_1 = sub(p_1, topleft)
        p_2 = sub(p_2, topleft)
        p_peak = (surf.get_width() / 2, 0)
        #pygame.draw.circle(surf, (50,255,50, 255), p_1, 10)
        #pygame.draw.circle(surf, (255,50,255,255), p_peak, 10)
        pygame.draw.circle(surf, playercolor, p_2, 10)
        _draw_parabola(surf, playercolor, p_peak, p_1, p_2)
        return surf, pygame.Rect(add(topleft,(0,-10)), (size[0],size[1]/2))
    
def _get_parabola(point, peak):
    t_point = (point[0] - peak[0], point[1] - peak[1])
    a = t_point[1]/t_point[0]**2
    return lambda x: a*x**2

def _draw_parabola(surface, color, peak, p1, p2):
    for point in (p1,p2):
        p = _get_parabola(point, peak)
        prev_point = (peak)
        for x in range(int(peak[0]), int(point[0]), 3 if peak[0] < point[0] else -3):
            next_point = (x, p(x-peak[0])+peak[1])
            pygame.draw.line(surface, color, prev_point, next_point, 2)
            prev_point = next_point
    