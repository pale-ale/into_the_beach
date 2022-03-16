from typing import TYPE_CHECKING

from itblib.abilities.base_abilities.toggle_ability_base import \
    ToggleAbilityBase
from itblib.gridelements.StatusEffects import StatusEffectBurrowed
from itblib.Log import log

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class BurrowAbility(ToggleAbilityBase):
    """
    Units can burrow themselves to not be affect by pushes,
    at the cost of losing all other means of movement until unborrwed again.
    """
    def __init__(self, unit: "UnitBase"):
        super().__init__(unit, 2)

    def on_trigger(self):
        """Burrows the unit."""
        super().on_trigger()
        owner = self.get_owner()
        if owner:
            effect = owner.get_statuseffect("Burrowed")
            if effect:
                owner.remove_statuseffect(effect)
            else:
                burroweffect = StatusEffectBurrowed(owner)
                owner.add_status_effect(burroweffect)
                log(f"BurrowAbility: Burrowed unit: {owner.name}", 0)
            owner.done = True
