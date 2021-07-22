from .GridElement import GridElement

class EffectBase(GridElement):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectTrees"):
        super().__init__(grid, pos, age, done, name)


class EffectFire(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectFire"):
        super().__init__(grid, pos, age, done, name)


class EffectMountain(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectMountain"):
        super().__init__(grid, pos, age, done, name)


class EffectRiver(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectRiver"):
        super().__init__(grid, pos, age, done, name)


class EffectWheat(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectWheat"):
        super().__init__(grid, pos, age, done, name)


class EffectTown(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectTown"):
        super().__init__(grid, pos, age, done, name)

class EffectHeal(EffectBase):
    def __init__(self, grid, pos:"tuple[int,int]", age=0.0, done=True, name="EffectHeal"):
        super().__init__(grid, pos, age, done, name)

