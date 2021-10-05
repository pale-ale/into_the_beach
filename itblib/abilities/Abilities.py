from typing import TYPE_CHECKING
from itblib.Globals.Enums import PREVIEWS
from itblib.gridelements.Effects import EffectBurrowed
from itblib.net.NetEvents import NetEvents
from itblib.abilities.AbilityBase import AbilityBase

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase


class RangedAttackAbility(AbilityBase):
    """A simple ranged attack, with a targeting scheme like the artillery in ITB."""

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 2, cooldown=2)

    def get_ordinals(self):
        x,y = self._unit.pos
        width = self._unit.grid.width
        height = self._unit.grid.height
        ordinals = set()
        for i in range (width):
            ordinals.add((i,y))
        for i in range (height):
            ordinals.add((x,i))
        ordinals.remove((x,y))
        return ordinals
    
    def on_select_ability(self):
        super().on_select_ability()
        pos = self._unit.pos
        coords = self.get_ordinals()
        coords = coords.difference(self._unit.grid.get_ordinal_neighbors(pos))
        #for coord in coords:
        #    self.area_of_effect.append(coord)

    def set_targets(self, targets:"list[tuple[int,int]]"):
        super().set_targets(targets)
        assert len(targets) == 1
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions:
            self.selected_targets = [target]
            self.area_of_effect.clear()

    def on_trigger(self):
        super().on_trigger()
        if len(self.selected_targets) > 0:
            damage = [self._unit.baseattack["physical"], "physical"]
            self._unit.attack(self.selected_targets[0], *damage)
    

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


class ObjectiveAbility(AbilityBase):
    """This ability makes a unit an "Objective", meaning the player loses if it dies."""
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit, 0, 0)

    def on_death(self):
        super().on_death()
        NetEvents.session.objective_lost(self._unit.ownerid)


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
