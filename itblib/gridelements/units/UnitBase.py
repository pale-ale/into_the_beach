from itblib.Serializable import Serializable
from typing import TYPE_CHECKING, Type
from itblib.gridelements.GridElement import GridElement
from itblib.gridelements.Effects import EffectBurrowed, EffectBleeding

if TYPE_CHECKING:
    from itblib.Grid import Grid
    from itblib.abilities.AbilityBase import AbilityBase
    from itblib.gridelements.Effects import StatusEffect

class UnitBase(GridElement, Serializable):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", ownerid:int, 
    name:str="Base", hitpoints:int=5, canswim:bool=False, abilities:"list[Type[AbilityBase]]"=[]):
        GridElement.__init__(self, grid, pos)
        Serializable.__init__(self, ["name", "_hitpoints", "ownerid", "statuseffects", "abilities"])
        self.name = name
        self._hitpoints = hitpoints
        self.defense = {"physical": 0, "magical": 0, "collision": 0}
        self.baseattack = {"physical": 1, "magical": 0}
        self.statuseffects:"list[StatusEffect]" = []
        self.canswim = canswim
        self.ownerid = ownerid
        self.moverange = 5
        self.orientation = "sw"
        self.abilities:"list[AbilityBase]" = [ability(self) for ability in abilities]
    
    def extract_data(self, custom_fields: "dict[str,any]" = ...) -> dict:
        customstatuseffects = [x.extract_data() for x in self.statuseffects]
        customabilities = [x.extract_data() for x in self.abilities]
        return Serializable.extract_data(self, custom_fields={"statuseffects":customstatuseffects, "abilities":customabilities})
    
    def insert_data(self, data):
        Serializable.insert_data(self, data, exclude=["statuseffects", "abilities"])
        for effectdata in data["statuseffects"]:
            for effectclass in [EffectBurrowed, EffectBleeding]:
                if effectclass.__name__ == "Effect" + effectdata["name"]:
                    self.add_statuseffect(effectclass(self))
        for abilitydata in data["abilities"]:
            #TODO: spawn the abilities, do not rely on the __init__ ones
            for ability in self.abilities:
                if type(ability).__name__ == abilitydata["name"]:
                    abilitydata["selected_targets"] = [(x,y) for x,y in abilitydata["selected_targets"]]
                    ability.insert_data(abilitydata, exclude=["name"])

    def tick(self, dt: float):
        super().tick(dt)
        for ability in self.abilities:
            ability.tick(dt)
    
    def add_ability(self, ability_class:"AbilityBase"):
        """Add an ability to this unit. Will spawn and initialize the required class."""
        for ability in self.abilities:
            if ability is ability_class:
                print(ability_class.__name__, "-class already exists")
                exit(1)
        self.abilities.append(ability_class(self))
    
    def add_statuseffect(self, statuseffect:"StatusEffect"):
        """Add a status effect."""
        self.statuseffects.append(statuseffect)
    
    def remove_statuseffect(self, statuseffect:"StatusEffect"):
        """Remove a status effect."""
        for se in self.statuseffects:
            if se == statuseffect:
                se.on_purge()
                self.statuseffects.remove(se)
                return
    
    def get_statuseffect(self, name:str) -> "StatusEffect|None":
        """Return the statuseffect with name name, or None if not found."""
        for se in self.statuseffects:
            if se.name == name:
                return se
        return None

    def remove_ability(self, ability_class_name:str):
        """Remove an ability by class name"""
        for ability in self.abilities[:]:
            if type(ability).__name__ == ability_class_name:
                print("Removed ability:", ability)
                self.abilities.remove(ability)
    
    def drown(self):
        """Called when a unit drowns."""
        print("I drowned :(")
        self.grid.remove_unit(self.pos)

    def attack(self, target:"tuple[int,int]", damage:int, damagetype:str):
        """Attack target position with damage amount and damage type."""
        unit = self.grid.get_unit(target)
        if unit:
            unit.change_hp(-damage, damagetype)
    
    def get_movement_ability(self):
        """Return the MovementAbility of this unit or None if it doesn't have one."""
        for ability in self.abilities[:]:
            if type(ability).__name__ == "MovementAbility":
                return ability
    
    def change_hp(self, delta_hp:int, hp_change_type:str):
        """Change hp by amount. Influenced by damage reduction etc.."""
        if delta_hp > 0:
            self._hitpoints += delta_hp
        else:
            reduceddamage = delta_hp + self.defense[hp_change_type]
            self._hitpoints += min(0,reduceddamage)
        if self._hitpoints <= 0:
            self.on_death()
    
    def on_update_abilities_phases(self, newphase:int):
        """Propagate a phase change to this unit's abilities."""
        for ability in self.abilities:
            ability.on_update_phase(newphase)
        for statuseffect in self.statuseffects:
            statuseffect.on_update_phase(newphase)
    
    def on_update_cursor(self, newcursorpos:"tuple[int,int]"):
        """Called when the user moves the cursor."""
        for ability in self.abilities:
            ability.on_update_cursor(newcursorpos)
    
    def on_select(self):
        """Called when this unit is selected."""
        for ability in self.abilities:
            ability.on_parentunit_select()
    
    def on_deselect(self):
        """Called when this unit is deselected."""
        for ability in self.abilities:
            ability.on_parentunit_deselect()
    
    def on_activate_ability(self, slot:int):
        """Called when the user wishes to use an ability by pressing one of the assigned slot numbers."""
        if slot >= 0 and slot < len(self.abilities):
            ability = self.abilities[slot]
            if ability.remainingcooldown == 0:
                ability.on_select_ability()

    def on_confirm_target(self, target:"tuple[int,int]"):
        """Called when the user hits enter, passes on the cursor position where the event occured."""
        for ability in self.abilities:
            if ability.selected:
                ability.confirm_target(target)
    
    def on_death(self):
        """Called when this unit's hitpoints are reduced to <= 0"""
        for ability in self.abilities:
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

    