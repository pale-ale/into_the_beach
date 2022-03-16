from abc import ABC, abstractmethod
from typing import Callable, Generator

import pygame
from itblib.abilities.baseAbilities.ability_base import AbilityBase
from itblib.ui.TextureManager import Textures


class AbilityPreviewBase(ABC):
    """Creates previews for a unit based on it's abilities and their targets."""

    def __init__(self, ability:AbilityBase) -> None:
        super().__init__()
        self._ability = ability
    
    @abstractmethod
    def get_blit_func(self, transform_func:Callable[["tuple[int,int]"], "tuple[int,int]"]) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        """@return: A generator yielding the blits to display this ability
        @transform_func: turns grid coordinates into screen coordinates
        """
    
    def _get_simple_preview_gen(self, transform_func:Callable[["tuple[int,int]"], "tuple[int,int]"]):
        """@transform_func: turns grid coordinates into screen coordinates
        """
        aoe = self._ability.area_of_effect
        for pos, preview_name in aoe:
            if preview_name != "Special":
                yield (
                    Textures.get_spritesheet(preview_name.replace(':',''))[0], 
                    pygame.Rect(transform_func(pos), (64,64)), 
                    pygame.Rect(0,0,64,64)
                )
