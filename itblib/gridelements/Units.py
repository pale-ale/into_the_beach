from typing import TYPE_CHECKING
from itblib.gridelements.GridElement import GridElement
from itblib.net.NetEvents import NetEvents
from itblib.gridelements.Effects import StatusEffect, EffectBleed
from itblib.Abilities import AbilityBase, HealAbility, \
    MovementAbility, \
    ObjectiveAbility, \
    PunchAbility, \
    PushAbility, \
    RangedAttackAbility

if TYPE_CHECKING:
    from itblib.Grid import Grid

class UnitBase(GridElement):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", ownerid:int, 
    name:str="UnitBase", hitpoints:int=5, canswim:bool=False):
        super().__init__(grid, pos)
        self.name = name
        self.hitpoints = hitpoints
        self.defense = {"physical": 0, "magical": 0, "collision": 0}
        self.baseattack = {"physical": 20, "magical": 0}
        self.statuseffects:"list[StatusEffect]" = []
        self.canswim = canswim
        self.ownerid = ownerid
        self.moverange = 5
        self.orientation = "sw"
        self.abilities:list[AbilityBase] = [MovementAbility(self), PunchAbility(self)]
    
    def tick(self, dt: float):
        super().tick(dt)
        for ability in self.abilities:
            ability.tick(dt)
    
    def add_ability(self, ability_class:AbilityBase):
        for ability in self.abilities:
            if ability is ability_class:
                print(ability_class.__name__, "-class already exists")
                exit(1)
        self.abilities.append(ability_class(self))
    
    def add_statuseffect(self, statuseffect:"StatusEffect"):
        self.statuseffects.append(statuseffect)

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
            if type(ability) is MovementAbility:
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
                ability.add_targets(targets)
    
    def on_death(self):
        for ability in self.abilities:
            ability.on_death()
        self.grid.remove_unit(self.pos)

    
class UnitSaucer(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="UnitSaucer"):
        super().__init__(grid, pos, ownerid, name=name)
        self.add_ability(RangedAttackAbility)
        self.add_ability(PushAbility)


class UnitMagician(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="m"):
        super().__init__(grid, pos, ownerid, name=name)


class UnitBarbarian(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="U"):
        super().__init__(grid, pos, ownerid, name=name)


class UnitBloodWraith(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="UnitBloodWraith"):
        super().__init__(grid, pos, ownerid, name=name)
        self.add_ability(HealAbility)
        
    def attack(self, target:"tuple[int,int]" , damage:int, damagetype:str):
        print("UnitBloodWraith: target:", target)
        unit = self.grid.get_unit(target)
        if unit:
            killingblow = unit.hitpoints > 0
            unit.on_change_hp(-1, "physical")
            if unit.hitpoints <= 0 and killingblow:
                self.on_change_hp(1,"physical")


class UnitHomebase(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="UnitCrystal"):
        super().__init__(grid, pos, ownerid, name=name)
        self.add_ability(ObjectiveAbility)
        self.remove_ability("MovementAbility")
        self.remove_ability("PunchAbility")


class UnitKnight(UnitBase):
      def __init__(self, grid, pos, ownerid, name:str="UnitKnight"):
        super().__init__(grid, pos, ownerid, name=name)

class UnitBurrower(UnitBase):
      def __init__(self, grid, pos, ownerid, name:str="UnitBurrower"):
        super().__init__(grid, pos, ownerid, name=name)
