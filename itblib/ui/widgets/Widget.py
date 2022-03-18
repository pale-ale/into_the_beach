from typing import Generator

import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.ui.IGraphics import IGraphics


class Widget(IGraphics, ComponentAcceptor):
    """A Graphical object with a size, hierarchy, transforms, etc."""
    def __init__(self) -> None:
        ComponentAcceptor.__init__(self)
        tfc = TransformComponent()
        tfc.attach_component(self)

    def get_size(self) -> tuple[int,int]:
        return self.image.get_size()

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        pos = self.get_component(TransformComponent).get_position()
        size = self.image.get_size()
        yield (self.image, pygame.Rect(pos, self.image.get_size()), ((0,0),size))

    @property 
    def parent(self) -> "ComponentAcceptor|None":
        """Widgets calculate their global positions as their parent's position + local offset"""
        parent_tfc = self.get_component(TransformComponent).parent_transform_component
        return parent_tfc.owner if parent_tfc else None

    @property
    def position(self) -> tuple[int,int]:
        """The local offset of a Widget"""
        return self.get_component(TransformComponent).relative_position

    @parent.setter 
    def parent(self, new_parent:"ComponentAcceptor"):
        self.get_component(TransformComponent).set_transform_target(new_parent)

    @position.setter
    def position(self, new_position:tuple[int,int]):
        self.get_component(TransformComponent).relative_position = new_position
