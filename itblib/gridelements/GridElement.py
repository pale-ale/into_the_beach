from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.Grid import Grid

class GridElement:
    "Class containing mainly positional and state data about an object on the grid."

    def __init__(self, grid:"Grid", pos:"tuple[int,int]", age:float=0.0, done:bool=True, name:str=""):
        self.grid = grid
        self.pos = pos
        self.age = age
        self.done = done
        self.name = name
    
    def tick(self, delta_time:float):
        self.age += delta_time

    def on_update_phase(self, new_phase:int):
        """Called when a phase change occured."""
        pass
