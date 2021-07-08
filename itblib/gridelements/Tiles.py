from itblib.gridelements.Units import UnitBase
from .GridElement import GridElement

class TileBase(GridElement):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.name = "TileDirt"
        self.onfire = False

    def on_enter(self, unit:UnitBase):
        pass

    def on_damage(self, damage:int):
        pass


class TileForest(TileBase):
    def __init__(self):
        super().__init__()
        self.name = "TileForest"
        self.id = 1

    def on_enter(self, unit:UnitBase):
        pass

    def on_damage(self, damage:int):
        self.onfire = True


class TileSea(TileBase):
    def __init__(self):
        super().__init__()
        self.id = 2

    def on_enter(self, unit:UnitBase):
        if not unit.canswim:
            unit.drown()
