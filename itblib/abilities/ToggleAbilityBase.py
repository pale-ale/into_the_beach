from itblib.abilities.AbilityBase import AbilityBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class ToggleAbilityBase(AbilityBase):
    def __init__(self, unit: "UnitBase", phase:int):
        super().__init__(unit, phase, 1)
        self._owning_component.targeting_ability = True
    
    def on_select_ability(self):
        owner = self.get_owner()
        if owner:
            self.confirm_target(owner, not self.primed)
    