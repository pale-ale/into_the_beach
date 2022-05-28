from typing import TYPE_CHECKING

from itblib.Vec import IVector2
if TYPE_CHECKING:
    from itblib.Grid import Grid

class GridElement:
    "Class containing mainly positional and state data about an object on the grid."

    def __init__(self, grid:"Grid", position:IVector2, age:float=0.0, done:bool=True, name:str=""):
        assert isinstance(position, IVector2)
        self.grid = grid
        self.position = position
        self.age = age
        self.done = done
        self.name = name
    
    def tick(self, delta_time:float):
        self.age += delta_time

    def on_update_phase(self, new_phase:int):
        """Called when a phase change occured."""
        pass
