from .GridElement import GridElement

class EffectBase(GridElement):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "EffectTrees"


class EffectFire(EffectBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "EffectFire"
        self.time = 0

class EffectMountain(EffectBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "EffectMountain"
        self.time = 0


class EffectRiver(EffectBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "EffectRiver"
        self.time = 0


class EffectWheat(EffectBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "EffectWheat"
        self.time = 0


class EffectTown(EffectBase):
    def __init__(self, grid):
        super().__init__(grid)
        self.name = "EffectTown"
        self.time = 0
