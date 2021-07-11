from .GridElement import GridElement
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.Grid import Grid
    from itblib.gridelements.Units import UnitBase

class TileBase(GridElement):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="TileDirt"):
        super().__init__(grid, pos, age, done, name)
        self.onfire = False

    def on_enter(self, unit:"UnitBase"):
        pass

    def on_damage(self, damage:int):
        pass


class TileForest(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="TileForest"):
        super().__init__(grid, pos, age, done, name)

    def on_enter(self, unit:"UnitBase"):
        pass

    def on_damage(self, damage:int):
        self.onfire = True


class TileSea(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="TileSea"):
        super().__init__(grid, pos, age, done, name)

    def on_enter(self, unit:"UnitBase"):
        if not unit.canswim:
            unit.drown()

class TileLava(TileBase):
    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age=0.0, done=True, name="TileLava"):
        super().__init__(grid, pos, age, done, name)
