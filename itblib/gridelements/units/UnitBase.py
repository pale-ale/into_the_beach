from itblib.Serializable import Serializable
from typing import TYPE_CHECKING, Type
from itblib.gridelements.GridElement import GridElement
from itblib.net.NetEvents import NetEvents
from itblib.gridelements.Effects import EffectBurrowed, EffectBleeding

if TYPE_CHECKING:
    from itblib.Grid import Grid
    from itblib.abilities.AbilityBase import AbilityBase
    from itblib.gridelements.Effects import StatusEffect

class UnitBase(GridElement, Serializable):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", ownerid:int, 
    name:str="Base", hitpoints:int=5, canswim:bool=False, abilities:"list[Type[AbilityBase]]"=[]):
        GridElement.__init__(self, grid, pos)
        Serializable.__init__(self, ["name", "hitpoints", "ownerid", "statuseffects"])
        self.name = name
        self.hitpoints = hitpoints
        self.defense = {"physical": 0, "magical": 0, "collision": 0}
        self.baseattack = {"physical": 20, "magical": 0}
        self.statuseffects:"list[StatusEffect]" = []
        self.canswim = canswim
        self.ownerid = ownerid
        self.moverange = 5
        self.orientation = "sw"
        self.abilities:"list[AbilityBase]" = [ability(self) for ability in abilities]
    
    def extract_data(self, custom_fields: "dict[str,any]" = ...) -> dict:
        customstatuseffects = [x.extract_data() for x in self.statuseffects]
        return Serializable.extract_data(self, custom_fields={"statuseffects":customstatuseffects})
    
    def insert_data(self, data):
        Serializable.insert_data(self, data)
        for effectdata in data["statuseffects"]:
            for effectclass in [EffectBurrowed, EffectBleeding]:
                if effectclass.__name__ == effectdata["name"]:
                    self.add_statuseffect(effectclass(self))

    def tick(self, dt: float):
        super().tick(dt)
        for ability in self.abilities:
            ability.tick(dt)
    
    def add_ability(self, ability_class:"AbilityBase"):
        for ability in self.abilities:
            if ability is ability_class:
                print(ability_class.__name__, "-class already exists")
                exit(1)
        self.abilities.append(ability_class(self))
    
    def add_statuseffect(self, statuseffect:"StatusEffect"):
        self.statuseffects.append(statuseffect)
    
    def remove_statuseffect(self, statuseffect:"StatusEffect"):
        for se in self.statuseffects:
            if se == statuseffect:
                se.on_purge()
                self.statuseffects.remove(se)
                return
    
    def get_statuseffect(self, name:str) -> "StatusEffect|None": 
        for se in self.statuseffects:
            if se.name == name:
                return se
        return None

    def remove_ability(self, ability_class_name:str):
        print("Removing ability:", ability_class_name)
        for ability in self.abilities[:]:
            if type(ability).__name__ == ability_class_name:
                print("Removed ability:", ability)
                self.abilities.remove(ability)
    
    def drown(self):
        print("I drowned :(")
        self.grid.remove_unit(self.pos)

    def attack(self, target:"tuple[int,int]", damage:int, damagetype:str):
        print("target", target)
        unit = self.grid.get_unit(target)
        if unit:
            unit.on_change_hp(-damage, damagetype)
    
    def get_movement_ability(self):
        for ability in self.abilities[:]:
            if ability.id == 0:
                return ability
    
    def on_change_hp(self, delta_hp:int, hp_change_type:str):
        if delta_hp > 0:
            self.hitpoints += delta_hp
        else:
            reduceddamage = delta_hp + self.defense[hp_change_type]
            self.hitpoints += min(0,reduceddamage)
        NetEvents.snd_netunithpchange(self.pos, self.hitpoints)
        if self.hitpoints <= 0:
            self.on_death()
    
    def on_update_abilities_phases(self, newphase:int):
        for ability in self.abilities:
            ability.on_update_phase(newphase)
        for statuseffect in self.statuseffects:
            statuseffect.on_update_phase(newphase)
    
    def on_update_cursor(self, newcursorpos:"tuple[int,int]"):
        for ability in self.abilities:
            ability.on_update_cursor(newcursorpos)
    
    def on_select(self):
        for ability in self.abilities:
            ability.on_parentunit_select()
    
    def on_deselect(self):
        for ability in self.abilities:
            ability.on_parentunit_deselect()
    
    def on_activate_ability(self, slot:int):
        if slot < len(self.abilities):
            ability = self.abilities[slot]
            if ability.remainingcooldown == 0:
                ability.on_select_ability()

    def on_targets_chosen(self, targets:"list[tuple[int,int]]"):
        for ability in self.abilities:
            if ability.selected:
                ability.set_targets(True, targets)
    
    def on_death(self):
        for ability in self.abilities:
            ability.on_death()
        self.grid.remove_unit(self.pos)
    
    def on_receive_shove(self, to:"tuple[int,int]"):
        if not self.grid.is_coord_in_bounds(to) or self.grid.is_space_empty(True, to):
            return
        if self.grid.is_space_empty(False, to):
            self.grid.move_unit(self.pos, to)
            self.get_movement_ability().selected_targets.clear()
        else:
            #we collide with a different unit or object
            targetint = self.grid.c_to_i(to)
            self.grid.units[targetint].on_change_hp(-1, "collision")
            newposint = self.grid.c_to_i(to)
            self.grid.units[newposint].on_change_hp(-1, "collision")

    