"""Contains the ToggleAbilitybase class."""

from typing import TYPE_CHECKING

from itblib.abilities.baseAbilities.ability_base import AbilityBase

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class ToggleAbilityBase(AbilityBase):
    """Derive to allow toggling an ability on or off."""
    def __init__(self, unit: "UnitBase", phase:int):
        super().__init__(unit, phase, 1)

    def on_select_ability(self):
        owner = self.get_owner()
        if owner:
            self.confirm_target(owner, not self.primed)

    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        return set()
