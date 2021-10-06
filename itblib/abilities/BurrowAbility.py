from typing import TYPE_CHECKING
from itblib.gridelements.Effects import EffectBurrowed
from itblib.abilities.ToggleAbilityBase import ToggleAbilityBase

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class BurrowAbility(ToggleAbilityBase):
    def __init__(self, unit: "UnitBase"):
        super().__init__(unit, 2)
    
    def on_trigger(self):
        super().on_trigger()
        effect = self._unit.get_statuseffect("EffectBurrowed")
        if effect:
            self._unit.remove_statuseffect(effect)
        else:
            burroweffect = EffectBurrowed(self._unit)
            self._unit.add_statuseffect(burroweffect)
            print("BurrowAbility: Burrowed unit:", self._unit.name)
        self._unit.done = True
