from GridElement import GridElement

class TileBase(GridElement):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.onfire = False

    def on_enter(self, unit):
        pass

    def on_damage(self, damage:int):
        pass


class TileForest(TileBase):
    def __init__(self):
        super().__init__()
        self.id = 1

    def on_enter(self, unit):
        print("test")

    def on_damage(self, damage:int):
        self.onfire = True


class TileSea(TileBase):
    def __init__(self):
        super().__init__()
        self.id = 2

    def on_enter(self, unit):
        if not unit.canswim:
            unit.drown()
