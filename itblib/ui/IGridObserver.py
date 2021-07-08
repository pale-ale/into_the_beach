from itblib.gridelements.Units import UnitBase
from itblib.gridelements.Effects import EffectBase
from itblib.gridelements.Tiles import TileBase
from itblib.Maps import Map


class IGridObserver:
    
    def on_add_tile(self, tile:TileBase):
        pass
    
    def on_add_effect(self, effect:EffectBase):
        pass

    def on_add_unit(self, unit:UnitBase):
        pass

    def on_remove_unit(self, pos:"tuple[int,int]"):
        pass

    def on_move_unit(self, src:"tuple[int,int]", dst:"tuple[int,int]"):
        pass

    def on_load_map(self, map:Map):
        pass