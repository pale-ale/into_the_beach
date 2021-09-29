from itblib.Serializable import Serializable
from itblib.gridelements.GridElement import GridElement
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.Grid import Grid
    from itblib.gridelements.units.UnitBase import UnitBase

class TileBase(GridElement, Serializable):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="Base"):
        # no super() because of multiple inheritance
        GridElement.__init__(self, grid, pos, age, done, name)
        Serializable.__init__(self, ["name"])
        self.onfire = False

    def on_enter(self, unit:"UnitBase"):
        pass

    def on_damage(self, damage:int):
        pass


class TileWater(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="Water"):
        super().__init__(grid, pos, age, done, name)

    def on_enter(self, unit:"UnitBase"):
        if not unit.canswim:
            unit.drown()


class TileLava(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="Lava"):
        super().__init__(grid, pos, age, done, name)
    
    def on_enter(self, unit:"UnitBase"):
        """Assuming that entering the Lava Tile would cause a unit damage."""
        pass


class TileRock(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="Rock"):
        super().__init__(grid, pos, age, done, name)
