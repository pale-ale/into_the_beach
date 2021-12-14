from typing import Generator
import pygame
import pygame.surface
import pygame.rect
import abc

class PerfSprite(abc.ABC):
    @abc.abstractmethod
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        pass
    
    def update(self, delta_time:float) -> None:
        pass