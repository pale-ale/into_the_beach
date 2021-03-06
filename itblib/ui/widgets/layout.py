"""Horizontal layouts can be used to display one or more Widgets or Surfaces next to each other."""

from typing import TYPE_CHECKING, Callable

import pygame
from pygame import Rect, Surface
from itblib.Vec import IVector2
from itblib.components import TransformComponent
from itblib.ui.widgets.ui_widget import Widget

if TYPE_CHECKING:
    from typing import Generator


class HorizontalLayoutSurface(Widget):
    """The non-Widget HorizontalLayout displays Surfaces next to each other, spaced by a margin."""
    def __init__(self):
        super().__init__()
        self._inner_padding = 1
        self.children:list[pygame.Surface] = []

    def get_screen_child_pos(self, child_index: int) -> IVector2:
        """Return the position of the child at index child_index."""
        pos = self.get_component(TransformComponent).get_position()
        offset = IVector2(0, 0)
        for child in self.children[:child_index]:
            offset = IVector2(offset.x + child.get_size()[0] + self._inner_padding, 0)
        return pos + offset

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        for i,child in enumerate(self.children):
            childsize = child.get_size()
            yield (
                child, 
                pygame.Rect(self.get_screen_child_pos(i).c, childsize),
                pygame.Rect((0,0), childsize)
            )

class HorizontalLayoutWidget(Widget):
    """
    The Widget HorizontalLayout displays Widgets next to each other, spaced by a margin,
    with some additional layout options.
    """

    def __init__(self, size:IVector2, center:tuple[bool,bool]=(True,True)):
        super().__init__()
        self._inner_padding_func:Callable[[int], int] = lambda i: 20 if i%2 else 1
        self.center_height, self.center_width = center
        self.desired_size = size

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children:"list[Widget]"):
        self._children = children
        self._layout_children()

    def _layout_children(self):
        content_height = 0
        content_width = 0
        for index, child in enumerate(self._children):
            child.parent = self
            content_height = max(content_height, child.get_size()[1])
            content_width += child.get_size()[0] + self._inner_padding_func(index)

        x_offset = (self.get_size().x - content_width)/2 if self.center_width  else 0
        current_x = 0
        for index, child in enumerate(self._children):
            y_offset = (self.get_size().y - child.get_size()[1])/2 if self.center_height else 0
            child.position = IVector2(int(x_offset + current_x), int(y_offset))
            current_x += child.get_size()[0] + self._inner_padding_func(index)

    def get_blits(self) -> "Generator[tuple[Surface, Rect, Rect]]":
        for child in self._children:
            yield from child.get_blits()

    def get_size(self):
        return self.desired_size
