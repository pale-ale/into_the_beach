from GridElement import GridElement

class EffectBase(GridElement):
    def __init__(self):
        super().__init__()
        self.id = 0


class EffectFire(EffectBase):
    def __init__(self):
        super().__init__()
        self.id = 1
        self.time = 0
