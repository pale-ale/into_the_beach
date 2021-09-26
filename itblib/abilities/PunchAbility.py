from typing import TYPE_CHECKING
from itblib.Globals.Enums import PREVIEWS
from itblib.abilities.TargetAbilityBase import TargetAbilityBase

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class PunchAbility(TargetAbilityBase):
    """A simple damaging ability. Deals damage to a neighboring target."""

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 1, 2, 0)

    def on_select_ability(self):
        super().on_select_ability()
        for neighbor in self._unit.grid.get_ordinal_neighbors(*self._unit.pos):
            self.area_of_effect.append((neighbor, PREVIEWS[0]))

    def apply_to_target(self, target: "tuple[int,int]"):
        super().apply_to_target(target)
        damage = [self._unit.baseattack["physical"], "physical"]
        self._unit.attack(self.selected_targets[0], *damage)
    