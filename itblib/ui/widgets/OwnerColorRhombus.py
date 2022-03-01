from typing import TYPE_CHECKING, Generator

import pygame
from itblib.components.TransformComponent import TransformComponent
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from playgrounds.itblib.ui.widgets.Widget import Widget

if TYPE_CHECKING:
    from itblib.gridelements.UnitsUI import UnitBaseUI

class OwnerColorRhombus(Widget):
    def __init__(self, playercolor:tuple[int,int,int,int]) -> None:
        super().__init__()
        self._tc = TransformComponent()
        self._tc.attach_component(self)
        self._unit = None
        self._player_color = playercolor
        x = 48
        y = 32
        self._unit_owner_square_size = (x,y)
        self._unit_owner_square_corners = [
            (int(x/2+.5),2),
            (x-3,int(y/2-.5)+1),  (x-3,int(y/2+.5)+1),  
            (int(x/2+.5),y-1),  (int(x/2-.5),y-1),
            (2,int(y/2+.5)+1),    (2,int(y/2-.5)+1),
            (int(x/2-.5),2)
            ]
        self._image = pygame.Surface(self._unit_owner_square_size).convert_alpha()
        self._image.fill(0)
        self._draw_lines()
        self._tc.relative_position = ((STANDARD_UNIT_SIZE[0]-x)/2,(STANDARD_UNIT_SIZE[1]-y)-8)

    def attach_to_unit(self, unit:"UnitBaseUI"):
        self._unit = unit
        self._tc.set_transform_target(unit)

    def _draw_lines(self):
        pygame.draw.lines(
            self._image,
            self._player_color,
            True,
            self._unit_owner_square_corners,
            1
        )

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self._image, pygame.Rect(self._tc.get_position(), self._image.get_size()), self._image.get_rect())
