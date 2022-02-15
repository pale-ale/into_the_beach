from typing import Generator

import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.ui.PerfSprite import PerfSprite
from itblib.Vec import add


class HorizontalLayout(ComponentAcceptor, PerfSprite):
    def __init__(self):
        ComponentAcceptor.__init__(self)
        self.tfc = TransformComponent()
        self.tfc.attach_component(self)
        self.inner_padding = 1
        self.children:list[pygame.Surface] = []
    
    def get_pos(self, i:int) -> "tuple[int,int]":
        pos = self.tfc.get_position()
        offset = (0, 0)
        for child in self.children[:i]:
            offset = (offset[0] + child.get_size()[0] + self.inner_padding, 0)
        return add(pos, offset)

    def update(self, delta_time: float) -> None:
        return super().update(delta_time)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        for i,child in enumerate(self.children):
            childsize = child.get_size()
            yield (child, pygame.Rect(self.get_pos(i), childsize), pygame.Rect((0,0), childsize))
