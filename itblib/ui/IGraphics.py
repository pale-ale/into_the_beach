from abc import ABC, abstractmethod
from typing import Generator

import pygame


class IGraphics(ABC):
    """Objects with this interface can be drawn to a surface."""

    @abstractmethod
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        pass
