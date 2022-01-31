from typing import TYPE_CHECKING
from itblib.gridelements.Effects import EffectBurrowed
from itblib.abilities.baseAbilities.ToggleAbilityBase import ToggleAbilityBase

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class BurrowAbility(ToggleAbilityBase):
    def __init__(self, unit: "UnitBase"):
        super().__init__(unit, 2)
    
    def on_trigger(self):
        super().on_trigger()
        owner = self.get_owner()
        if owner:
            effect = owner.get_statuseffect("Burrowed")
            if effect:
                owner.remove_statuseffect(effect)
            else:
                burroweffect = EffectBurrowed(owner)
                owner.add_statuseffect(burroweffect)
                print("BurrowAbility: Burrowed unit:", owner.name)
            owner.done = True
