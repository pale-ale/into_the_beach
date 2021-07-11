from itblib.gridelements.Units import UnitBase
from .GridElement import GridElement

class TileBase(GridElement):
    def __init__(self, grid):
        super().__init__(grid)
        self.id = 0
        self.name = "TileDirt"
        self.onfire = False

    def on_enter(self, unit:UnitBase):
        pass

    def on_damage(self, damage:int):
        pass


class TileForest(TileBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "TileForest"
        self.id = 1

    def on_enter(self, unit:UnitBase):
        pass

    def on_damage(self, damage:int):
        self.onfire = True


class TileSea(TileBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "TileSea"
        self.id = 2

    def on_enter(self, unit:UnitBase):
        if not unit.canswim:
            unit.drown()

class TileLava(TileBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "TileLava"
        self.id = 3
