"""Provides the AbilityPreviewBase class."""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame
from itblib.Vec import IVector2
from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.ui.TextureManager import Textures

if TYPE_CHECKING:
    from typing import Callable, Generator

class AbilityPreviewBase(ABC):
    """Creates previews for a unit based on it's abilities and their targets."""

    def __init__(self, ability:AbilityBase) -> None:
        super().__init__()
        self._ability = ability

    @abstractmethod
    def get_blit_func(self, transform_func:"Callable[[tuple[int,int]], tuple[int,int]]") -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        """@return: A generator yielding the blits to display this ability
        @transform_func: turns grid coordinates into screen coordinates
        """

    def _get_simple_preview_gen(self, transform_func:"Callable[[IVector2], IVector2]"):
        """@transform_func: turns grid coordinates into screen coordinates
        """
        aoe = self._ability.area_of_effect
        for aoe_tile in aoe:
            position, preview_name = aoe_tile
            assert isinstance(position, IVector2)
            if preview_name != "Special":
                yield (
                    Textures.get_spritesheet(preview_name.replace(':',''))[0],
                    pygame.Rect(transform_func(position).c, (64,64)),
                    pygame.Rect(0,0,64,64)
                )
