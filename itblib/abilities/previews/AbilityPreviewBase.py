from abc import ABC, abstractmethod
from typing import Callable, Generator
from itblib.abilities.AbilityBase import AbilityBase
from itblib.ui.TextureManager import Textures
import pygame

class AbilityPreviewBase(ABC):
    """Creates previews for a unit based on it's abilities and their targets."""

    def __init__(self, ability:AbilityBase) -> None:
        super().__init__()
        self._ability = ability
    
    @abstractmethod
    def get_blit_func(self, transform_func:Callable[["tuple[int,int]"], "tuple[int,int]"]) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        """@transform_func: turns grid coordinates into screen coordinates"""
    
    def _get_simple_preview_gen(self, transform_func:Callable[["tuple[int,int]"], "tuple[int,int]"]):
        """@transform_func: turns grid coordinates into screen coordinates"""
        aoe = self._ability.area_of_effect
        for pos, preview_name in aoe:
            if not preview_name.startswith("Special"):
                yield (
                    Textures.textures[preview_name][0], 
                    pygame.Rect(transform_func(pos), (64,64)), 
                    pygame.Rect(0,0,64,64)
                )