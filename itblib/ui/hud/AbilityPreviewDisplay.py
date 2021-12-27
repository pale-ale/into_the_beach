from itblib.abilities.AbilityBase import AbilityBase
from itblib.ui.GridUI import GridUI
from itblib.ui.PerfSprite import PerfSprite
import pygame
from typing import Generator
from itblib.gridelements.units.UnitBase import UnitBase

from itblib.abilities.previews.RangedAttackAbilityPreview import RangedAttackAbilityPreview
from itblib.abilities.previews.SimpleAbilityPreview import SimpleAbilityPreview

class AbilityPreviewDisplay(PerfSprite):
    """Creates previews for a unit based on it's abilities and their targets."""

    def __init__(self, gridui:GridUI) -> None:
        super().__init__()
        self.unit:"UnitBase|None" = None
        self._gridui = gridui
        self._ability_preview_classes = [SimpleAbilityPreview, RangedAttackAbilityPreview]

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        for ability in self.unit.ability_component._abilities:
            if ability:
                preview = self._get_preview_class(ability)(ability)
                yield from preview.get_blit_func(self._gridui.transform_grid_screen)
    
    def update(self, delta_time: float) -> None:
        pass

    def _get_preview_class(self, ability:AbilityBase):
        ability_name = type(ability).__name__
        for abiliy_preview_class in self._ability_preview_classes:
            if abiliy_preview_class.__name__ == ability_name + "Preview":
                return abiliy_preview_class
        return SimpleAbilityPreview
