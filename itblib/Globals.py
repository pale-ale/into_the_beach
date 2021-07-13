from .gridelements.Units import UnitBase, UnitSaucer, UnitHomebase
from .gridelements.Effects import EffectBase, EffectFire, EffectMountain, EffectRiver, EffectWheat, EffectTown
from .gridelements.Tiles import *

class ClassMapping:
    tileclassmapping = {
        0:None,
        1:TileBase,
        2:TileForest,
        3:TileSea,
        4:TileLava,
        5:TileRock
    }
    effectclassmapping = {
        0:None,
        1:EffectBase,
        2:EffectFire,
        3:EffectMountain,
        4:EffectRiver,
        5:EffectWheat,
        6:EffectTown
    }
    unitclassmapping = {
        0:None,
        1:UnitBase,
        2:UnitSaucer,
        3:UnitHomebase
    }
