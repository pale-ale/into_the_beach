from typing import TYPE_CHECKING

from itblib.abilities.base_abilities.target_ability_base import TargetAbilityBase
from itblib.gridelements.StatusEffects import StatusEffectBleeding

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class SerrateAbility(TargetAbilityBase):
    """Deals 1 damage to a unit and causes bleeding."""

    def __init__(self, unit: "UnitBase"):
        super().__init__(unit, 3, 1)
   
    def apply_to_target(self, target: "tuple[int,int]"):
        super().apply_to_target(target)
        owner = self.get_owner()
        if owner:
            owner.attack(target, 1, "physical")
            u = owner.grid.get_unit(target)
            if u:
                u.add_status_effect(StatusEffectBleeding(u))

    def _get_valid_targets(self) -> "set[tuple[int,int]]|None":
        owner = self.get_owner()
        if owner:
            pos = owner.pos
            return owner.grid.get_neighbors(pos)
            