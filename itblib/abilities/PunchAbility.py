from typing import TYPE_CHECKING

from itblib.abilities.baseAbilities.TargetAbilityBase import TargetAbilityBase
from itblib.globals.Constants import PREVIEWS

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class PunchAbility(TargetAbilityBase):
    """A simple damaging ability. Deals damage to a neighboring target."""

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 3, 5)

    def apply_to_target(self, target: "tuple[int,int]"):
        super().apply_to_target(target)
        owner = self.get_owner()
        damage = [owner.baseattack["physical"], "physical"]
        owner.attack(self.selected_targets[0], *damage)
