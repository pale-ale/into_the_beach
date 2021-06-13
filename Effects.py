from GridElement import GridElement

class EffectBase(GridElement):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.name = "EffectTrees"


class EffectFire(EffectBase):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.name = "EffectFire"
        self.time = 0
