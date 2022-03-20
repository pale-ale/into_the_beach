"""
World Effects are effects that can be placed in the world, i.e.
are not necessarily bound to a unit or tile but rather a position.
"""

from itblib.globals.Constants import PHASES
from itblib.gridelements.GridElement import GridElement
from itblib.Serializable import Serializable
from itblib.ui.IDisplayable import IDisplayable


class WorldEffectBase(GridElement, Serializable, IDisplayable):
    """The base class for any World Effect"""
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Trees"):
        GridElement.__init__(self, grid, pos, age, done, name)
        Serializable.__init__(self, ["name"])

    def on_spawn(self):
        """Triggers when the effect is spawned, i.e. placed on the world"""

    def get_display_name(self) -> str:
        return self.name


class EffectFire(WorldEffectBase):
    """Deals damage over time."""
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Fire"):
        super().__init__(grid, pos, age, done, name)

    def on_update_phase(self, new_phase: int):
        """Deal 1 physical damage to unit on this field."""
        super().on_update_phase(new_phase)
        if new_phase == PHASES.BATTLEPHASE:
            unit = self.grid.get_unit(self.pos)
            if unit:
                unit.change_hp(-1, "physical")

    def get_display_description(self) -> str:
        return "Units on top will take 1 fire damage each battle phase."


class EffectMountain(WorldEffectBase):
    """Blocks certain movement types."""
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Mountain"):
        super().__init__(grid, pos, age, done, name)

    def get_display_description(self) -> str:
        return "Blocks movement and provides limited cover."


class EffectRiver(WorldEffectBase):
    """Currently does nothing."""
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="River"):
        super().__init__(grid, pos, age, done, name)

    def get_display_description(self) -> str:
        return "No effects."


class EffectWheat(WorldEffectBase):
    """Currently does nothing."""
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Wheat"):
        super().__init__(grid, pos, age, done, name)

    def get_display_description(self) -> str:
        return "Easily flammable."


class EffectTown(WorldEffectBase):
    """Currently does nothing."""
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="Town"):
        super().__init__(grid, pos, age, done, name)

    def get_display_description(self) -> str:
        return "No effects."


class EffectHeal(WorldEffectBase):
    """Heals a unit on this square by 1 and purges Bleeding."""
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

    def tick(self, delta_time:float):
        super().tick(delta_time)
        if self.age >= 2:
            self.done = True
            self.grid.remove_worldeffect(self, self.pos)

    def get_display_description(self) -> str:
        return ""


class EffectStartingArea(WorldEffectBase):
    """A player can only deploy units in his starting area at the beginning of a match."""
    def __init__(self, grid, pos: "tuple[int,int]", age=0, done=True, name="StartingArea"):
        super().__init__(grid, pos, age, done, name)
        self.serializable_fields.append("ownerid")
        self.ownerid:int

    def get_display_description(self) -> str:
        return "Units can be deployed here."

    def on_update_phase(self, new_phase: int):
        super().on_update_phase(new_phase)
        if new_phase > 0:
            self.grid.remove_worldeffect(self, self.pos)
