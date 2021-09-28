from itblib.gridelements.Effects import EffectBleeding
from typing import TYPE_CHECKING
from itblib.abilities.TargetAbilityBase import TargetAbilityBase
from itblib.net.NetEvents import NetEvents

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class SerrateAbility(TargetAbilityBase):
    """Causes a unit take 1 damage and be inflicted with bleeding."""
    def __init__(self, unit: "UnitBase"):
        super().__init__(unit, 1, 2)
   
    def apply_to_target(self, target: "tuple[int,int]"):
        super().apply_to_target(target)
        self._unit.attack(target, 1, "physical")
        u = self._unit.grid.get_unit(target)
        if u:
            u.add_statuseffect(EffectBleeding(u))