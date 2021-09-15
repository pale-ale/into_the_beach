from itblib.abilities.MovementAbility import MovementAbility
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.abilities.Abilities import PunchAbility, RangedAttackAbility,\
    PushAbility,\
    HealAbility,\
    ObjectiveAbility,\
    BurrowAbility

class UnitSaucer(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="UnitSaucer"):
        super().__init__(grid, pos, ownerid, name=name, 
            abilities=[
                MovementAbility,
                RangedAttackAbility,
                PushAbility
            ]
        )


class UnitBloodWraith(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="UnitBloodWraith"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[HealAbility])
        
    def attack(self, target:"tuple[int,int]" , damage:int, damagetype:str):
        unit = self.grid.get_unit(target)
        if unit:
            killingblow = unit.hitpoints > 0
            unit.on_change_hp(-1, "physical")
            if unit.hitpoints <= 0 and killingblow:
                self.on_change_hp(1,"physical")


class UnitHomebase(UnitBase):
    def __init__(self, grid, pos, ownerid, name:str="UnitCrystal"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[ObjectiveAbility])


class UnitKnight(UnitBase):
      def __init__(self, grid, pos, ownerid, name:str="UnitKnight"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[MovementAbility, PunchAbility])


class UnitBurrower(UnitBase):
      def __init__(self, grid, pos, ownerid, name:str="UnitBurrower"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[BurrowAbility])
