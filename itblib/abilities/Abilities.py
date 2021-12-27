from typing import TYPE_CHECKING

from itblib.abilities.AbilityBase import AbilityBase
from itblib.components.AbilityComponent import AbilityComponent
from itblib.globals.Enums import PREVIEWS
from itblib.net.NetEvents import NetEvents

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class RangedAttackAbility(AbilityBase):
    """A simple ranged attack, with a targeting scheme like the artillery in ITB."""

    def __init__(self, owning_component:"AbilityComponent"):
        super().__init__(owning_component=owning_component, phase=2, cooldown=2)
    
    def on_select_ability(self):
        super().on_select_ability()
        for coord in self._get_valid_targets():
            self.area_of_effect.add((coord, PREVIEWS[0]))

    def set_targets(self, targets:"list[tuple[int,int]]"):
        assert len(targets) == 1, f"Invalid targets: {targets}"
        super().set_targets(targets)
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions:
            self.selected_targets = [target]
            self.area_of_effect.clear()
  
    def on_trigger(self):
        super().on_trigger()
        owner = self.get_owner()
        if owner and len(self.selected_targets) > 0:
            damage = [owner.baseattack["physical"], "physical"]
            self.get_owner().attack(self.selected_targets[0], *damage)
    
    def confirm_target(self, target: "tuple[int,int]", primed=True):
        if self._is_valid_target(target):
            self.selected_targets = [target]
            super().confirm_target(target, primed=primed)
            self.area_of_effect = {(target, PREVIEWS[-1])}
    
    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        owner = self.get_owner()
        if owner:
            pos = owner.pos
            coords = self._get_ordinals(pos, owner.grid.size)
            coords = coords.difference(owner.grid.get_neighbors(pos))
        return coords
    
    def _get_ordinals(self, origin:"tuple[int,int]", dimensions:"tuple[int,int]"):
        x,y = origin
        ordinals:"set[tuple[int,int]]" = set()
        for i in range (dimensions[0]):
            ordinals.add((i,y))
        for i in range (dimensions[1]):
            ordinals.add((x,i))
        ordinals.remove((x,y))
        return ordinals
    

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


class HealAbility(AbilityBase):
    """Spawn a heal at selected neighboring tile, healing any unit by 1 and purging bleeding."""
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 2, cooldown=3)
        self.remainingcooldown = 0
    
    def on_select_ability(self):
        super().on_select_ability()
        pos = self._unit.pos
        for neighbor in self._unit.grid.get_ordinal_neighbors(pos):
            self.area_of_effect.append((neighbor, PREVIEWS[0]))

    def add_targets(self, targets:"list[tuple[int,int]]"):
        super().add_targets(targets)
        assert len(targets) == 1
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions or NetEvents.connector.authority:
            self.selected_targets = [target]
            self.area_of_effect.clear()
            self.on_deselect_ability()
            NetEvents.snd_netabilitytarget(self)
            
    def activate(self):
        if len(self.selected_targets) > 0 and NetEvents.connector.authority:
            super().activate()
            self._unit.grid.add_worldeffect(self.selected_targets[0], 7, True)
            self.area_of_effect.clear()
            self.selected_targets.clear()
