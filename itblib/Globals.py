from .gridelements.Units import UnitBase,\
                                UnitSaucer,\
                                UnitBloodWraith,\
                                UnitHomebase
from .gridelements.Effects import EffectBase,\
                                EffectFire,\
                                EffectMountain,\
                                EffectRiver,\
                                EffectWheat,\
                                EffectTown,\
                                EffectHeal
from .gridelements.Tiles import *

class ClassMapping:
    """
    A handy map to quickly obtain the correct classes needed when loading a map containing
    the respective ids.
    """
    
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
        6:EffectTown,
        7:EffectHeal,
    }
    _unitclasses = [None, UnitBase, UnitSaucer, UnitBloodWraith, UnitHomebase]
    unitidclassmapping = {}
    unitclassidmapping = {}
    for i in range(len(_unitclasses)):
        unitidclassmapping[i] = _unitclasses[i]
        unitclassidmapping[_unitclasses[i]] = i
