"""Contains the AbilityPreviewDisplay class."""

from typing import TYPE_CHECKING

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.abilities.base_abilities.cone_ability_base import ConeAbilityBase
from itblib.abilities.base_abilities.ranged_abliity_base import \
    RangedAbilityBase
from itblib.abilities.previews.cone_ability_preview import \
    ConeAttackAbilityPreview
from itblib.abilities.previews.ranged_ability_preview import \
    RangedAttackAbilityPreview
from itblib.abilities.previews.simple_ability_preview import SimpleAbilityPreview
from itblib.ui.IGraphics import IGraphics

if TYPE_CHECKING:
    import pygame
    from typing import Generator
    from itblib.gridelements.units.UnitBase import UnitBase
    from itblib.ui.GridUI import GridUI


class AbilityPreviewDisplay(IGraphics):
    """Creates previews for a unit based on it's abilities and their targets."""

    def __init__(self, gridui:"GridUI") -> None:
        super().__init__()
        self.unit:"UnitBase|None" = None
        self._gridui = gridui

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        for ability in self.unit.ability_component._abilities:
            if ability:
                preview = self._get_preview_class(ability)(ability)
                yield from preview.get_blit_func(self._gridui.transform_grid_screen)

    def update(self, delta_time: float) -> None:
        pass

    def _get_preview_class(self, ability:AbilityBase):
        if isinstance(ability, ConeAbilityBase):
            return ConeAttackAbilityPreview
        if isinstance(ability, RangedAbilityBase):
            return RangedAttackAbilityPreview
        return SimpleAbilityPreview
