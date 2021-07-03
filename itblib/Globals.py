from .gridelements.Units import UnitBase, UnitSaucer, UnitHomebase
from .gridelements.Effects import EffectBase, EffectFire
from .gridelements.Tiles import *

class ClassMapping:
    tileclassmapping = {
        0:None,
        1:TileBase,
        2:TileForest,
        3:TileSea
    }
    effectclassmapping = {
        0:None,
        1:EffectBase,
        2:EffectFire
    }
    unitclassmapping = {
        0:None,
        1:UnitBase,
        2:UnitSaucer,
        3:UnitHomebase
    }