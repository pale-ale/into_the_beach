from typing import Text
from pygame import image
import pygame
from Units import UnitBase
from Effects import EffectBase, EffectFire
from Tiles import *

class Textures:
    texturepath = "./sprites/"
    textures = {"Units":{}, "Tiles":{}, "Effects":{}, "Other":{}}

    @classmethod
    def get_spritesheet(cls, unitname:str, animname:str, orientation:str):
        return cls.textures["Units"][unitname][animname][orientation]

    @staticmethod
    def get_texture_key(gridelementname:str, animname:str, orientation:str, framenumber:int=0):
        assert orientation in ["ne","se","sw","nw"] and framenumber >= 0
        return gridelementname + orientation.upper() + animname + framenumber + ".png"

    @staticmethod 
    def loadtextures():
        LoaderMethods.prepare_unit_texture_space(Textures.textures["Units"], "UnitBase", "Idle")
        LoaderMethods.load_unit_textures(Textures.textures["Units"], "UnitBase", "Idle", "ne", 1)
        LoaderMethods.load_unit_textures(Textures.textures["Units"], "UnitBase", "Idle", "se", 1)
        LoaderMethods.load_unit_textures(Textures.textures["Units"], "UnitBase", "Idle", "sw", 1)
        LoaderMethods.load_unit_textures(Textures.textures["Units"], "UnitBase", "Idle", "nw", 1)
        # Filenames are built the following way:
        #       <UnitName> + <Orientation> + <AnimationName> + <Framenumber(>=0)> + .png
        # e.g.: UnitSaucer + SW            + Idle            + 0                  + .png
        # => UnitSaucerSWIdle1.png

        # load the files into textures once, then use them all over the game
        # this could take a while, depending on the amount of image data to load

    selectionpreviewtexture = "SelectionPreview.png"
    movementpreviewtexture = "MovementPreview.png"
    targetmovementpreviewtexture = "TargetMovementPreview.png"
    

    # Textures have the same name as the texture they point to, without the extension
    # e.g.: UnitSaucerSWIdle

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


class LoaderMethods():
    @staticmethod
    def prepare_unit_texture_space(indict:dict, unitname:str, animname:str):
        if unitname not in indict.keys():
            indict[unitname] = {}
        if animname not in indict[unitname].keys():
            indict[unitname][animname] = {}
        for orientation in ["ne","se","sw","nw"]:
            if orientation not in indict[unitname][animname].keys():
                indict[unitname][animname][orientation] = []

    def load_unit_textures(indict:dict, unitname:str, animname:str, orientation:str, framecount:int=1):
        for i in range(framecount):
            path = Textures.texturepath + unitname + orientation.upper() + animname + str(i) + ".png"
            print(f"Loading '{path}'")
            indict[unitname][animname][orientation].append(pygame.image.load(path))


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
    
