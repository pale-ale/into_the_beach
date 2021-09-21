from .gridelements.units.Units import UnitBase, UnitKnight, UnitBurrower,\
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
    
    _effectclasses = [
        None, EffectBase, EffectFire, EffectMountain, EffectRiver, EffectWheat,
        EffectTown, EffectHeal
    ]
    _unitclasses = [None, UnitBase, UnitSaucer, UnitBloodWraith, UnitHomebase, UnitKnight, UnitBurrower]
    _tileclasses = [None, TileBase, TileWater, TileLava, TileRock]
    unitidclassmapping = {}
    unitclassidmapping = {}
    for i in range(len(_unitclasses)):
        unitidclassmapping[i] = _unitclasses[i]
        unitclassidmapping[_unitclasses[i]] = i
    tileidclassmapping = {}
    tileclassidmapping = {}
    for i in range(len(_tileclasses)):
        tileidclassmapping[i] = _tileclasses[i]
        tileclassidmapping[_tileclasses[i]] = i
    effectidclassmapping = {}
    effectclassidmapping = {}
    for i in range(len(_effectclasses)):
        effectidclassmapping[i] = _effectclasses[i]
        effectclassidmapping[_effectclasses[i]] = i
