from Units import UnitBase
from Effects import EffectBase, EffectFire
from Tiles import *

class Textures:
    texturepath = "./sprites/"
    tiletexturemapping = {
        0:["TileDirt.png"],
        1:["TileForest.png"],
        2:["TileWater.png"]
    }
    effecttexturemapping = {
        0:["EffectTrees.png"],
        1:["EffectFire1.png", "EffectFire2.png"]
    }
    unittexturemapping = {
        0:["Unit1.png","Unit2.png","Unit3.png","Unit4.png"]
    }

class Classes:
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
        0:UnitBase
    }
    