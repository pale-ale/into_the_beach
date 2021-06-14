from pygame import image
import pygame
from Units import UnitBase, UnitSaucer
from Effects import EffectBase, EffectFire
from Tiles import *

class Textures:
    texturepath = "./sprites/"
    textures = {"Units":{}, "Tiles":{}, "Effects":{}, "Other":{}}

    @classmethod
    def get_spritesheet(cls, type:str, name:str, animname:str, orientation:str="sw"):
        if type == "Unit":
            return cls.textures["Units"][name][animname][orientation]
        if type == "Tile":
            return cls.textures["Tiles"][name][animname]
        if type == "Effect":
            return cls.textures["Effects"][name][animname]
    
    @staticmethod
    def loadtextures():
        unitdict = Textures.textures["Units"]
        LoaderMethods.prepare_unit_texture_space(unitdict, "UnitBase", "Idle")
        [LoaderMethods.load_unit_textures(unitdict, "UnitBase", "Idle", o, 1)
            for o in ["ne","se","sw","nw"]]
        LoaderMethods.prepare_unit_texture_space(unitdict, "UnitSaucer", "Idle")
        [LoaderMethods.load_unit_textures(unitdict, "UnitSaucer", "Idle", o, 2)
            for o in ["sw"]]
        
        tiledict = Textures.textures["Tiles"]
        LoaderMethods.prepare_tile_effect_texture_space(tiledict, "TileForest", "Default")
        LoaderMethods.load_tile_effect_textures(tiledict, "TileForest", "Default")
        LoaderMethods.prepare_tile_effect_texture_space(tiledict, "TileDirt", "Default")
        LoaderMethods.load_tile_effect_textures(tiledict, "TileDirt", "Default")
        
        effectdict = Textures.textures["Effects"]
        LoaderMethods.prepare_tile_effect_texture_space(effectdict, "EffectFire", "Default")
        LoaderMethods.load_tile_effect_textures(effectdict, "EffectFire", "Default", 2)
        
        effectdict = Textures.textures["Effects"]
        LoaderMethods.prepare_tile_effect_texture_space(effectdict, "EffectTrees", "Default")
        LoaderMethods.load_tile_effect_textures(effectdict, "EffectTrees", "Default")
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
    
    @staticmethod
    def prepare_tile_effect_texture_space(indict:dict, name:str, animname:str):
        if name not in indict.keys():
            indict[name] = {}
        if animname not in indict[name].keys():
            indict[name][animname] = []

    @staticmethod
    def load_unit_textures(indict:dict, unitname:str, animname:str, orientation:str, framecount:int=1):
        for i in range(framecount):
            path = Textures.texturepath + unitname + orientation.upper() + animname + str(i) + ".png"
            print(f"Loading '{path}'")
            indict[unitname][animname][orientation].append(pygame.image.load(path))
   
    @staticmethod
    def load_tile_effect_textures(indict:dict, name:str, animname:str, framecount:int=1):
        for i in range(framecount):
            path = Textures.texturepath + name + animname + str(i) + ".png"
            print(f"Loading '{path}'")
            indict[name][animname].append(pygame.image.load(path))


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
        1:UnitSaucer
    }
    