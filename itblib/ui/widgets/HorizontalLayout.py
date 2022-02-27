from typing import Generator

import pygame
from itblib.components.TransformComponent import TransformComponent
from itblib.ui.widgets.Widget import Widget
from itblib.Vec import add


class HorizontalLayout(Widget):
    def __init__(self):
        super().__init__()
        self._inner_padding = 1
        self.children:list[pygame.Surface] = []
    
    def get_screen_child_pos(self, child_index:int) -> "tuple[int,int]":
        pos = self.get_component(TransformComponent).get_position()
        offset = (0, 0)
        for child in self.children[:child_index]:
            offset = (offset[0] + child.get_size()[0] + self._inner_padding, 0)
        return add(pos, offset)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        for i,child in enumerate(self.children):
            childsize = child.get_size()
            yield (child, pygame.Rect(self.get_screen_child_pos(i), childsize), pygame.Rect((0,0), childsize))
