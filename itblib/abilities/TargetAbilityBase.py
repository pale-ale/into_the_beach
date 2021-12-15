from typing import TYPE_CHECKING

from itblib.abilities.AbilityBase import AbilityBase
from itblib.globals.Enums import PREVIEWS

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class TargetAbilityBase(AbilityBase):
    """Base class for any simple targeted ability, allowing for easy creation of such abilities."""

    def on_select_ability(self):
        super().on_select_ability()
        owner = self.get_owner()
        for neighbor in owner.grid.get_ordinal_neighbors(owner.pos):
            self.area_of_effect.add((neighbor, PREVIEWS[0]))
    
    def apply_to_target(self, target:"tuple[int,int]"):
        """Convenient override to act on each selected target."""
        pass

    def on_trigger(self):
        super().on_trigger()
        for target in self.selected_targets:
            self.apply_to_target(target)

    def set_targets(self, targets:"list[tuple[int,int]]"):
        super().set_targets(targets)
        self.area_of_effect.clear()
        self.on_deselect_ability()

    def confirm_target(self, target:"tuple[int,int]"):
        self.set_targets([target])
        super().confirm_target(target)
