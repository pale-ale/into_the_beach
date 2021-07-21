from typing import TYPE_CHECKING
from .GridElement import GridElement
from ..Abilities import AbilityBase, \
    MovementAbility, \
    ObjectiveAbility, \
    PunchAbility, \
    PushAbility, \
    RangedAttackAbility 

if TYPE_CHECKING:
    from ..Grid import Grid

class UnitBase(GridElement):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", ownerid:int, 
    playerid:int=0, name:str="UnitBase", hitpoints:int=5, canswim:bool=False):
        super().__init__(grid, pos)
        self.name = name
        self.hitpoints = hitpoints
        self.defense = {"physical": 0, "magical": 0, "collision": 0}
        self.baseattack = {"physical": 4, "magical": 0}
        self.canswim = canswim
        self.ownerid = ownerid
        self.moverange = 5
        self.orientation = "sw"
        self.userActions ={1:None, 2:None, 3:None, 4:None}
        self.abilities:list[AbilityBase] = [MovementAbility(self), PunchAbility(self)]
        self.player = playerid
    
    def tick(self, dt: float):
        super().tick(dt)
        for ability in self.abilities:
            ability.tick(dt)
    
    def add_ability(self, ability_class:AbilityBase):
        for ability in self.abilities:
            if ability is ability_class:
                print(ability_class.__name__, "-class lready exists")
                exit(1)
        self.abilities.append(ability_class(self))

    def remove_ability(self, ability_class_name:str):
        print("Removing ability:", ability_class_name)
        for ability in self.abilities[:]:
            if type(ability).__name__ == ability_class_name:
                print("Removed ability:", ability)
                self.abilities.remove(ability)
    
    def drown(self):
        print("I drowned :(")
        self.grid.remove_unit(*self.pos)

    def attack(self, target:"tuple[int,int]", damage:int, damagetype:str):
        print("target", target)
        unit = self.grid.get_unit(target)
        if unit:
            unit.on_take_damage(damage, damagetype)
    
    def get_movement_ability(self):
        for ability in self.abilities[:]:
            if type(ability) is MovementAbility:
                return ability
    
    def on_take_damage(self, damage:int, damagetype:str):
        reduceddamage = damage - self.defense[damagetype]
        self.hitpoints -= max(0,reduceddamage)
        if self.hitpoints <= 0:
            self.on_death()
    
    def on_update_abilities_phases(self, newphase:int):
        for ability in self.abilities:
            ability.on_update_phase(newphase)
    
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
            self.abilities[slot].on_select_ability()

    def on_targets_chosen(self, targets:"list[tuple[int,int]]"):
        for ability in self.abilities:
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


class UnitHomebase(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="UnitCrystal"):
        super().__init__(grid, pos, ownerid, name=name)
        self.add_ability(ObjectiveAbility)
        self.remove_ability("MovementAbility")
        self.remove_ability("PunchAbility")
