from itblib.abilities.AbilityBase import AbilityBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class ToggleAbilityBase(AbilityBase):
    def __init__(self, unit: "UnitBase", id:int, phase:int):
        super().__init__(unit, id, phase)
    
    def on_select_ability(self):
        super().on_select_ability()
        self.set_targets(not self.primed, [])
    