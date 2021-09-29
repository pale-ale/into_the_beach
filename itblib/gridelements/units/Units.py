from itblib.abilities.SerrateAbility import SerrateAbility
from itblib.abilities.MovementAbility import MovementAbility
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.abilities.PunchAbility import PunchAbility
from itblib.abilities.BurrowAbility import BurrowAbility
from itblib.abilities.Abilities import RangedAttackAbility,\
    PushAbility,\
    HealAbility,\
    ObjectiveAbility

class UnitSaucer(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="Saucer"):
        super().__init__(grid, pos, ownerid, name=name, 
            abilities=[
                MovementAbility,
                RangedAttackAbility,
                PushAbility
            ]
        )


class UnitBloodWraith(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="BloodWraith"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[HealAbility, MovementAbility, SerrateAbility])
        
    def attack(self, target:"tuple[int,int]" , damage:int, damagetype:str):
        unit = self.grid.get_unit(target)
        if unit:
            killingblow = unit.hitpoints > 0
            super().attack(target, damage, damagetype)
            if unit.hitpoints <= 0 and killingblow:
                self.on_change_hp(1,"physical")


class UnitHomebase(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="Homebase"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[ObjectiveAbility])


class UnitKnight(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="Knight"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[MovementAbility, PunchAbility])


class UnitBurrower(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="Burrower"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[BurrowAbility, MovementAbility, PunchAbility])