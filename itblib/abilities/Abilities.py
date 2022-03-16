from typing import TYPE_CHECKING

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.globals.Constants import PREVIEWS
from itblib.net.NetEvents import NetEvents

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class PushAbility(AbilityBase):
    """A melee attack pushing a target away from the attacker."""

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 3, cooldown=2)

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
        pos = self._unit.pos
        for neighbor in self._unit.grid.get_ordinal_neighbors(pos):
            self.area_of_effect.append((neighbor, PREVIEWS[0]))

    def on_trigger(self):
        super().on_trigger()
        if len(self.selected_targets):
            targetpos = self.selected_targets[0]
            unitposx, unitposy = self._unit.pos
            newpos = (2*targetpos[0]-unitposx, 2*targetpos[1]-unitposy)
            targetunit = self._unit.grid.get_unit(targetpos)
            targetunit.on_receive_shove(newpos)
        self.selected_targets.clear()
        self.area_of_effect.clear()

    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        owner = self.get_owner()
        return set(owner.grid.get_neighbors(owner.pos))


class ObjectiveAbility(AbilityBase):
    """This ability makes a unit an "Objective", meaning the player loses if it dies."""
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 0, 0)

    def on_death(self):
        super().on_death()
        NetEvents.session.objective_lost(self.get_owner().ownerid)
    
    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        return set()
