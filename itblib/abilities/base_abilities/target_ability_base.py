"""Contains the TargetAbilityBase class"""

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.globals.Constants import PREVIEWS

class TargetAbilityBase(AbilityBase):
    """Base class for any simple targeted ability, allowing for easy creation of such abilities."""

    def apply_to_target(self, target:"tuple[int,int]"):
        """Convenient override to act on each selected target."""

    def confirm_target(self, target: "tuple[int,int]", primed=True):
        if target in self._get_valid_targets():
            self.set_targets([target])
        return super().confirm_target(target, primed)

    def on_select_ability(self):
        super().on_select_ability()
        for neighbor in self._get_valid_targets():
            self.area_of_effect.add((neighbor, PREVIEWS[0]))

    def on_trigger(self):
        super().on_trigger()
        for target in self.selected_targets:
            self.apply_to_target(target)

    def set_targets(self, targets:"list[tuple[int,int]]"):
        super().set_targets(targets)
        self.on_deselect_ability()

    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        owner = self.get_owner()
        if owner:
            return owner.grid.get_neighbors(owner.pos)
        return set()
