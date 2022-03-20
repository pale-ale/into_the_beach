from abc import ABC, abstractmethod
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.gridelements.world_effects import WorldEffectBase
from itblib.gridelements.Tiles import TileBase
from itblib.Maps import Map


class IGridObserver(ABC):
    @abstractmethod
    def on_add_tile(self, tile:TileBase):
        pass
    
    @abstractmethod
    def on_add_unit(self, unit:UnitBase):
        pass

    @abstractmethod
    def on_add_worldeffect(self, effect:WorldEffectBase):
        pass

    @abstractmethod
    def on_remove_tile(self, pos:"tuple[int,int]"):
        pass

    @abstractmethod
    def on_remove_unit(self, pos:"tuple[int,int]"):
        pass
    
    @abstractmethod
    def on_remove_worldeffect(self, effect:WorldEffectBase, pos:"tuple[int,int]"):
        pass

    @abstractmethod
    def on_move_unit(self, src:"tuple[int,int]", dst:"tuple[int,int]"):
        pass

    @abstractmethod
    def on_remake_grid(self):
        pass

    @abstractmethod
    def on_change_phase(self, phase:int):
        pass