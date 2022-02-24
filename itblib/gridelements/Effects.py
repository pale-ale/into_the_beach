from itblib.globals.Constants import PHASES
from itblib.gridelements.GridElement import GridElement
from itblib.Serializable import Serializable
from itblib.ui.IDisplayable import IDisplayable

class EffectBase(GridElement, Serializable, IDisplayable):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Trees"):
        GridElement.__init__(self,grid, pos, age, done, name)
        Serializable.__init__(self, ["name"])
    
    def on_spawn(self):
        """Triggers when the effect is spawned, i.e. placed on the world"""
        pass

    def get_display_name(self) -> str:
        return self.name

  
class EffectFire(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Fire"):
        super().__init__(grid, pos, age, done, name)
    
    def on_update_phase(self, new_phase: int):
        super().on_update_phase(new_phase)
        if new_phase == PHASES.BATTLEPHASE:
            unit = self.grid.get_unit(self.pos)
            if unit:
                unit.change_hp(-1, "physical")
    
    def get_display_description(self) -> str:
        return "Units on top will take 1 fire damage each battle phase."


class EffectMountain(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Mountain"):
        super().__init__(grid, pos, age, done, name)
    
    def get_display_description(self) -> str:
        return "Blocks movement and provides limited cover."


class EffectRiver(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="River"):
        super().__init__(grid, pos, age, done, name)
    
    def get_display_description(self) -> str:
        return "No effects."


class EffectWheat(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Wheat"):
        super().__init__(grid, pos, age, done, name)
    
    def get_display_description(self) -> str:
        return "Easily flammable."


class EffectTown(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Town"):
        super().__init__(grid, pos, age, done, name)

    def get_display_description(self) -> str:
        return "No effects."


class EffectHeal(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=False, name="Heal"):
        super().__init__(grid, pos, age, done, name)
        self.done = False
    
    def on_spawn(self):
        super().on_spawn()
        unit = self.grid.get_unit(self.pos)
        if unit:
            unit.change_hp(1, "magic")
            bleed = unit.get_statuseffect("Bleeding")
            if bleed:
                unit.remove_statuseffect(bleed)

    def tick(self, dt:float):
        super().tick(dt)
        if self.age >= 2:
            self.done = True
            self.grid.remove_worldeffect(self, self.pos)
    
    def get_display_description(self) -> str:
        return ""
