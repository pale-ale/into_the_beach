from abc import ABC
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.gridelements.Effects import EffectBase
from itblib.gridelements.Tiles import TileBase
from itblib.Maps import Map


class IGridObserver(ABC):
    
    def on_add_tile(self, tile:TileBase):
        pass
    
    def on_add_unit(self, unit:UnitBase):
        pass

    def on_add_worldeffect(self, effect:EffectBase):
        pass

    def on_remove_tile(self, pos:"tuple[int,int]"):
        pass

    def on_remove_unit(self, pos:"tuple[int,int]"):
        pass
    
    def on_remove_worldeffect(self, effect:EffectBase, pos:"tuple[int,int]"):
        pass

    def on_move_unit(self, src:"tuple[int,int]", dst:"tuple[int,int]"):
        pass

    def on_load_map(self, map:Map):
        pass

    def on_change_phase(self, phase:int):
        pass