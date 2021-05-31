from GridElement import GridElement

class UnitBase(GridElement):
    def __init__(self, grid, name:str="p", hitpoints:int=5, canswim:bool=False):
        super().__init__()
        self.name = name
        self.hitpoints = hitpoints
        self.canswim = canswim
        self.grid = grid

    def drown(self):
        print("I drowned :(")
        self.grid.remove_unit(*self.pos)
