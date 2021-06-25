from GridElement import GridElement
from Abilities import MovementAbility, PunchAbility, RangedAttackAbility, PushAbility

class UnitBase(GridElement):
    def __init__(self, grid, ownerid, name:str="UnitBase", hitpoints:int=5, canswim:bool=False):
        super().__init__()
        self.name = name
        self.hitpoints = hitpoints
        self.defense = {"physical": 0, "magical": 0, "collision": 0}
        self.baseattack = {"physical": 4, "magical": 0}
        self.canswim = canswim
        self.grid = grid
        self.id = 0
        self.ownerid = ownerid
        self.moverange = 5
        self.orientation = "sw"
        self.actionhooks = dict()
        self.userActions ={1:None, 2:None, 3:None, 4:None}
        self.abilities = {"MovementAbility":MovementAbility(self), 
            "PunchAbility":PunchAbility(self),
            "RangedAttackAbility":RangedAttackAbility(self),
            "PushAbility":PushAbility(self)
        }
    
    def tick(self, dt: float):
        super().tick(dt)
        for ability in self.abilities.values():
            ability.tick(dt)
    
    def register_hook(self, hookname, function):
        if hookname == "UserAction":
            for slot in self.userActions.keys():
                if not self.userActions[slot]:
                    self.userActions[slot] = function
                    return
            print("Couldn't register UserAction: No free slots available for", self.name)
            return
        if hookname not in self.actionhooks.keys():
            self.actionhooks[hookname] = [function]
            return
        self.actionhooks[hookname].append(function)
    
    def trigger_hook(self, hookname, *args):
        if hookname.startswith("UserAction"):
            ability = self.userActions[int(hookname[-1])]
            if ability:
                ability(*args)
                return 1
        elif hookname in self.actionhooks:
            for hook in self.actionhooks[hookname]:
                hook(*args)
            return len(self.actionhooks[hookname])
        print(hookname, "has no bound actions")
        return 0  

    def drown(self):
        print("I drowned :(")
        self.grid.remove_unit(*self.pos)

    def attack(self, target, damage:int, damagetype:str):
        if self.grid.get_unit(*target):
            self.grid.units[self.grid.width*(target[1]) + target[0]].on_take_damage(damage, damagetype)
    
    def on_take_damage(self, damage:int, damagetype:str):
        reduceddamage = damage - self.defense[damagetype]
        self.hitpoints -= max(0,reduceddamage)
        if self.hitpoints <= 0:
            self.dying()
    
    def dying(self):
        print("I died :(")
        self.grid.remove_unit(*self.get_position())
    
class UnitSaucer(UnitBase):
    def __init__(self, grid, ownerid, name:str="UnitSaucer"):
        super().__init__(grid, ownerid, name)


class UnitMagician(UnitBase):
    def __init__(self, grid, ownerid, name:str="m"):
        super().__init__(grid, ownerid, name)


class UnitBarbarian(UnitBase):
    def __init__(self, grid, ownerid, name:str="b"):
        super().__init__(grid, ownerid, name)
