from typing import Callable, Generator

import pygame
from itblib.abilities.baseAbilities.RangedAttackAbilityBase import \
    RangedAttackAbility
from itblib.abilities.previews.AbilityPreviewBase import AbilityPreviewBase


class SimpleAbilityPreview(AbilityPreviewBase):
    """Creates previews for a unit based on it's abilities and their targets."""

    def __init__(self, ability: RangedAttackAbility) -> None:
        super().__init__(ability)
  
    def get_blit_func(self, transform_func:Callable[["tuple[int,int]"], "tuple[int,int]"]) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        """@transform_func: turns grid coordinates into screen coordinates"""
        yield from self._get_simple_preview_gen(transform_func=transform_func)
    
    def update(self, delta_time: float) -> None:
        pass
