from itblib.DamageReceiver import DamageReceiver
from itblib.Serializable import Serializable
from typing import TYPE_CHECKING, Type
from itblib.components.AbilityComponent import AbilityComponent
from itblib.gridelements.GridElement import GridElement
from itblib.gridelements.Effects import EffectBurrowed, EffectBleeding
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.abilities.MovementAbility import MovementAbility
from itblib.gridelements.UnitsUI import UnitBaseUI

if TYPE_CHECKING:
    from itblib.Grid import Grid
    from itblib.abilities.AbilityBase import AbilityBase
    from itblib.gridelements.Effects import StatusEffect

class UnitBase(GridElement, DamageReceiver, Serializable, ComponentAcceptor):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", ownerid:int, 
    name:str="Base", hitpoints:int=5, canswim:bool=False, abilities:"list[Type[AbilityBase]]"=[]):
        GridElement.__init__(self, grid, pos)
        DamageReceiver.__init__(self, hitpoints, hitpoints)
        Serializable.__init__(self, ["name", "_hitpoints", "ownerid", "statuseffects", "ability_component"])
        ComponentAcceptor.__init__(self)
        self.ability_component = AbilityComponent(abilities=abilities)
        self.ability_component.attach_component(self)
        self.name = name
        self.baseattack = {"physical": 1, "magical": 0}
        self.statuseffects:"list[StatusEffect]" = []
        self.canswim = canswim
        self.ownerid = ownerid
        self.orientation = "sw"
        self.observer:UnitBaseUI = None
    
    def extract_data(self, custom_fields: "dict[str,any]" = ...) -> dict:
        customstatuseffects = [x.extract_data() for x in self.statuseffects]
        return Serializable.extract_data(self, custom_fields={"statuseffects":customstatuseffects})
    
    def insert_data(self, data):
        Serializable.insert_data(self, data, exclude=["statuseffects", "ability_component", "_hitpoints"])
        for effectdata in data["statuseffects"]:
            for effectclass in [EffectBurrowed, EffectBleeding]:
                if effectclass.__name__ == "Effect" + effectdata["name"] and self.get_statuseffect(effectdata["name"]) is None:
                    self.add_statuseffect(effectclass(self))
        self.ability_component.insert_data(data["ability_component"])
        self.set_hp(data["_hitpoints"])

    def add_statuseffect(self, statuseffect:"StatusEffect"):
        """Add a status effect."""
        self.statuseffects.append(statuseffect)
        if self.observer:
            self.observer.on_add_statuseffect(statuseffect)
    
    def remove_statuseffect(self, statuseffect:"StatusEffect"):
        """Remove a status effect."""
        for se in self.statuseffects:
            if se == statuseffect:
                se.on_purge()
                self.statuseffects.remove(se)
                if self.observer:
                    self.observer.on_remove_statuseffect(statuseffect)
                return
    
    def get_statuseffect(self, name:str) -> "StatusEffect|None":
        """Return the statuseffect with name name, or None if not found."""
        for se in self.statuseffects:
            if se.name == name:
                return se
        return None
    
    def drown(self):
        """Called when a unit drowns."""
        print("I drowned :(")
        self.grid.remove_unit(self.pos)

    def attack(self, target:"tuple[int,int]", damage:int, damagetype:str):
        """Attack target position with damage amount and damage type."""
        unit = self.grid.get_unit(target)
        if unit:
            unit.change_hp(-damage, damagetype)
    
    def get_movement_ability(self) -> "MovementAbility|None":
        """Return the MovementAbility of this unit or None if it doesn't have one."""
        return self.ability_component.get_ability(MovementAbility)
    
    def on_update_phase(self, new_phase: int):
        super().on_update_phase(new_phase)
        for statuseffect in self.statuseffects:
            statuseffect.on_update_phase(new_phase)
        self.ability_component.on_update_abilities_phases(new_phase)
    
    def on_death(self):
        """Called when this unit's hitpoints are reduced to <= 0"""
        for ability in self.ability_component._abilities:
            ability.on_death()
        self.grid.remove_unit(self.pos)
    
    def on_receive_shove(self, to:"tuple[int,int]"):
        """Called when a shoving attack hits this unit, trying to push it to "to"."""
        if not self.grid.is_coord_in_bounds(to) or self.grid.is_space_empty(True, to):
            return
        if self.grid.is_space_empty(False, to):
            self.grid.move_unit(self.pos, to)
            self.get_movement_ability().selected_targets.clear()
        else:
            #we collide with a different unit or object
            targetint = self.grid.c_to_i(to)
            self.grid.units[targetint].change_hp(-1, "collision")
            newposint = self.grid.c_to_i(to)
            self.grid.units[newposint].change_hp(-1, "collision")

    