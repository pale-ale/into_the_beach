from GridElement import GridElement
from Abilities import MovementAbility

class UnitBase(GridElement):
    def __init__(self, grid, name:str="p", hitpoints:int=5, canswim:bool=False):
        super().__init__()
        self.name = name
        self.hitpoints = hitpoints
        self.canswim = canswim
        self.grid = grid
        self.id = 0
        self.moverange = 2
        self.actionhooks = dict()
        self.abilities = {"MovementAbility":MovementAbility(self)}
    
    def register_hook(self, hookname, function):
        if hookname not in self.actionhooks:
            self.actionhooks[hookname] = [function]
            return
        self.actionhooks[hookname].append(function)
    
    def trigger_hook(self, hookname):
        if hookname in self.actionhooks:
            for hook in self.actionhooks[hookname]:
                hook()
            return len(self.actionhooks[hookname])
        return 0  

    def drown(self):
        print("I drowned :(")
        self.grid.remove_unit(*self.pos)

    def attack(self, target, damage:int):
        if self.grid.get_unit(*target):
            self.grid.units[self.grid.width*(target[1]) + target[0]].on_take_damage(damage)
    
    def on_take_damage(self, damage:int):
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