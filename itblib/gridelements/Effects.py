from typing import TYPE_CHECKING
from itblib.gridelements.GridElement import GridElement
from itblib.Serializable import Serializable
if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class EffectBase(GridElement, Serializable):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectTrees"):
        GridElement.__init__(self,grid, pos, age, done, name)
        Serializable.__init__(self, ["name"])
    
    def on_spawn(self):
        """Triggers when the effect is spawned, i.e. placed on the world"""
        pass

  
class EffectFire(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectFire"):
        super().__init__(grid, pos, age, done, name)


class EffectMountain(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectMountain"):
        super().__init__(grid, pos, age, done, name)


class EffectRiver(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectRiver"):
        super().__init__(grid, pos, age, done, name)


class EffectWheat(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectWheat"):
        super().__init__(grid, pos, age, done, name)


class EffectTown(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectTown"):
        super().__init__(grid, pos, age, done, name)


class EffectHeal(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=False, name="EffectHeal"):
        super().__init__(grid, pos, age, done, name)
        self.done = False
    
    def on_spawn(self):
        super().on_spawn()
        unit = self.grid.get_unit(self.pos)
        if unit:
            unit.on_change_hp(5, "magic")

    def tick(self, dt:float):
        super().tick(dt)
        if self.age >= 1:
            self.done = True
            self.grid.remove_tileeffect(self, self.pos)


class StatusEffect(Serializable):
    def __init__(self, target:GridElement, name:str):
        super().__init__(["name"])
        self.target = target
        self.name = name
    
    def on_update_phase(self, newphase:int):
        "Triggers when the phase changes"
        pass

    def on_purge(self):
        "Triggers when the effect is removed from a unit"
        pass


class EffectBleeding(StatusEffect):
    def __init__(self, target: GridElement):
        super().__init__(target, name="EffectBleeding")
    
    def on_update_phase(self, newphase: int):
        super().on_update_phase()
        if newphase == 3:
            self.target.hitpoints -= 1


class EffectBurrowed(StatusEffect):
    def __init__(self, target: GridElement):
        super().__init__(target, name="EffectBurrowed")
        self.original_shove = target.on_receive_shove
        self.original_moverange = target.moverange
        target.moverange = 0
        target.on_receive_shove = self.disabled_shove
    
    def disabled_shove(self, pos):
        "Placeholder method to disable the unit's standard shove method"
        return
    
    def on_purge(self):
        self.target.on_receive_shove = self.original_shove
        self.target.moverange = self.original_moverange

