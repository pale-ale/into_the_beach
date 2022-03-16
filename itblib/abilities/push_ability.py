"""Contains the PushAbility class."""

from typing import TYPE_CHECKING

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.globals.Constants import PREVIEWS

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class PushAbility(AbilityBase):
    """A melee attack pushing a target away from the attacker."""

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 3, cooldown=2)

    #pylint: disable=missing-function-docstring,attribute-defined-outside-init
    def set_targets(self, targets:"list[tuple[int,int]]"):
        super().set_targets(targets)
        assert len(targets) == 1
        positions = [x[0] for x in self.area_of_effect]
        target = targets[0]
        if target in positions:
            self.selected_targets = [target]
        self.area_of_effect.clear()

    def on_select_ability(self):
        super().on_select_ability()
        owner = self.get_owner()
        if owner:
            pos = owner.pos
            for neighbor in owner.grid.get_neighbors(pos):
                self.area_of_effect.add((neighbor, PREVIEWS[0]))

    def on_trigger(self):
        super().on_trigger()
        owner = self.get_owner()
        if self.selected_targets and owner:
            targetpos = self.selected_targets[0]
            unitposx, unitposy = owner.pos
            newpos = (2*targetpos[0]-unitposx, 2*targetpos[1]-unitposy)
            targetunit = owner.grid.get_unit(targetpos)
            targetunit.on_receive_shove(newpos)
        self.selected_targets.clear()
        self.area_of_effect.clear()

    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        owner = self.get_owner()
        return set(owner.grid.get_neighbors(owner.pos))
