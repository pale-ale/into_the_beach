from .gridelements.Units import UnitBase, UnitSaucer, UnitHomebase
from .gridelements.Effects import EffectBase, EffectFire
from .gridelements.Tiles import *

class ClassMapping:
    tileclassmapping = {
        0:TileBase,
        1:TileForest,
        2:TileSea
    }
    effectclassmapping = {
        0:EffectBase,
        1:EffectFire
    }
    unitclassmapping = {
        0:UnitBase,
        1:UnitSaucer,
        2:UnitHomebase
    }
