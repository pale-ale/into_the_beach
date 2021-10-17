from itblib.abilities.AbilityBase import AbilityBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class ToggleAbilityBase(AbilityBase):
    def __init__(self, unit: "UnitBase", phase:int):
        super().__init__(unit, phase, 1)
    
    def on_select_ability(self):
        self.confirm_target(self._unit.pos,  not self.primed)
    