from pygame import image
from Units import UnitBase
from Effects import EffectBase, EffectFire
from Tiles import *

class Textures:
    @staticmethod
    def get_texture_key(gridelementname:str, orientation:str, animname:str, framenumber:int=0):
        assert orientation in ["ne","se","sw","nw"] and framenumber >= 0
        return gridelementname + orientation.capitalize() + animname + framenumber + ".png"

    texturepath = "./sprites/"
    selectionpreviewtexture = "SelectionPreview.png"
    movementpreviewtexture = "MovementPreview.png"
    targetmovementpreviewtexture = "TargetMovementPreview.png"
    # Filenames are built the following way:
    #       <UnitName> + <Orientation> + <AnimationName> + <Framenumber(>=0)> + .png
    # e.g.: UnitSaucer + SW            + Idle            + 0                  + .png
    # => UnitSaucerSWIdle1.png
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
        0:["Unit1.png","Unit2.png","Unit3.png","Unit4.png"],
        1:["UnitMagician1.png","UnitMagician2.png","UnitMagician3.png","UnitMagician4.png"],
        2:["UnitBarbarian1.png","UnitBarbarian2.png","UnitBarbarian3.png","UnitBarbarian4.png"]
    }
    unitanimationmapping = {
        0:["UnitSaucerIdle1.png", "UnitSaucerIdle2.png"]
    }
    abilitytexturemapping = {
        0:"MoveAbility.png",
        1:"PunchAbility.png"
    }


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
        0:UnitBase
    }
    
