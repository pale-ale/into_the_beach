from typing import TYPE_CHECKING
from .GridElement import GridElement
if TYPE_CHECKING:
    from itblib.gridelements.Units import UnitBase

class EffectBase(GridElement):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectTrees"):
        super().__init__(grid, pos, age, done, name)
    
    def on_spawn(self):
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


class StatusEffect:
    def __init__(self, target:GridElement, name:str):
        self.target = target
        self.name = name
    
    def on_update_phase(newphase:int):
        pass


class EffectBleed(StatusEffect):
    def __init__(self, target):
        super().__init__(target, name="EffectBleed")
    
    def on_update_phase(self, newphase: int):
        super().on_update_phase()
        if newphase == 3:
            self.target.hitpoints -= 1
            