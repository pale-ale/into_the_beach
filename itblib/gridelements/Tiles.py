from abc import ABC
from typing import TYPE_CHECKING

from itblib.globals.Constants import FLAGS
from itblib.gridelements.GridElement import GridElement
from itblib.Serializable import Serializable

if TYPE_CHECKING:
    from itblib.Grid import Grid
    from itblib.gridelements.units.UnitBase import UnitBase

class TileBase(GridElement, Serializable, ABC):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="Base"):
        GridElement.__init__(self, grid, pos, age, done, name)
        Serializable.__init__(self, ["name"])
    
    def get_movement_requirements(self):
        return FLAGS.MOVEMENT_DEFAULT

    def on_enter(self, unit:"UnitBase"):
        pass

    def on_damage(self, damage:int):
        pass


class TileDirt(TileBase):
    def __init__(self, grid: "Grid", pos: "tuple[int,int]", age=0, done=True, name="Dirt"):
        super().__init__(grid, pos, age=age, done=done, name=name)


class TileWater(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="Water"):
        super().__init__(grid, pos, age, done, name)

    def on_enter(self, unit:"UnitBase"):
        if not unit.canswim:
            unit.drown()
    
    def get_movement_requirements(self):
        return FLAGS.MOVEMENT_DEFAULT & FLAGS.MOVEMENT_WATER


class TileLava(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="Lava"):
        super().__init__(grid, pos, age, done, name)
    
    def on_enter(self, unit:"UnitBase"):
        """Assuming that entering the Lava Tile would cause a unit damage."""
        pass

    def get_movement_requirements(self):
        return FLAGS.MOVEMENT_DEFAULT & FLAGS.MOVEMENT_WATER

class TileRock(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="Rock"):
        super().__init__(grid, pos, age, done, name)

    def get_movement_requirements(self):
        return FLAGS.MOVEMENT_DEFAULT & FLAGS.MOVEMENT_MOUNTAIN