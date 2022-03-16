from typing import TYPE_CHECKING
from itblib.abilities.baseAbilities.target_ability_base import TargetAbilityBase

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class HealAbility(TargetAbilityBase):
    """Spawn a heal at selected neighboring tile, healing any unit by 1 and purging bleeding."""
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 2, cooldown=3)
        self.remainingcooldown = 0

    def apply_to_target(self, target: "tuple[int,int]"):
        super().apply_to_target(target)
        o = self.get_owner()
        if o:
            o.grid.add_worldeffect(self.selected_targets[0], 7)
