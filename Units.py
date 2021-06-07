from GridElement import GridElement

class UnitBase(GridElement):
    def __init__(self, grid, name:str="p", hitpoints:int=5, canswim:bool=False):
        super().__init__()
        self.name = name
        self.hitpoints = hitpoints
        self.canswim = canswim
        self.grid = grid
        self.id = 0

    def drown(self):
        print("I drowned :(")
        self.grid.remove_unit(*self.pos)

    def attack(self, target, damage:int):
        self.grid.units[self.grid.width*(target[1]) + target[0]].being_attacked(damage)
    
    def being_attacked(self, damage:int):
        self.hitpoints -= damage
        if self.hitpoints <= 0:
            self.dying()
    
    def dying(self):
        print("I died :(")
        self.grid.remove_unit(*self.pos)


class UnitMagician(UnitBase):
    def __init__(self, grid, name:str="m"):
        super().__init__(grid, name)
        self.id = 1


class UnitBarbarian(UnitBase):
    def __init__(self, grid, name:str="b"):
        super().__init__(grid, name)
        self.id = 2