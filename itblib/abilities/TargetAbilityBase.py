from itblib.abilities.AbilityBase import AbilityBase
from typing import TYPE_CHECKING
from itblib.Globals.Enums import PREVIEWS

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class TargetAbilityBase(AbilityBase):
    """Base class for any simple targeted ability, allowing for easy creation of such abilities."""

    def on_select_ability(self):
        super().on_select_ability()
        for neighbor in self._unit.grid.get_ordinal_neighbors(*self._unit.pos):
            self.area_of_effect.append((neighbor, PREVIEWS[0]))
    
    def apply_to_target(self, target:"tuple[int,int]"):
        """Convenient override to act on each selected target."""
        pass

    def on_trigger(self):
        super().on_trigger()
        for target in self.selected_targets:
            self.apply_to_target(target)

    def set_targets(self, primed:bool, targets:"list[tuple[int,int]]"):
        super().set_targets(primed, targets)
        self.area_of_effect.clear()
        self.on_deselect_ability()
