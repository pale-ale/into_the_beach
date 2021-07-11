import pygame
from ..Enums import PREVIEWS

class Textures:
    texturepath = "./sprites/"
    textures = {"Units":{}, "Tiles":{}, "Effects":{}, "Other":{}}

    @classmethod
    def get_spritesheet(cls, type:str, name:str, animname:str, orientation:str="sw") -> "list[pygame.Surface]":
        if type == "Unit":
            return cls.textures["Units"][name][animname][orientation]
        if type == "Tile":
            return cls.textures["Tiles"][name][animname]
        if type == "Effect":
            return cls.textures["Effects"][name][animname]
    
    @staticmethod
    def load_textures():
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
        LoaderMethods.prepare_tile_effect_texture_space(tiledict, "TileLava", "Default")
        LoaderMethods.load_tile_effect_textures(tiledict, "TileLava", "Default")
        
        effectdict = Textures.textures["Effects"]
        LoaderMethods.prepare_tile_effect_texture_space(effectdict, "EffectFire", "Default")
        LoaderMethods.load_tile_effect_textures(effectdict, "EffectFire", "Default", 2)
        LoaderMethods.prepare_tile_effect_texture_space(effectdict, "EffectTrees", "Default")
        LoaderMethods.load_tile_effect_textures(effectdict, "EffectTrees", "Default")
        LoaderMethods.prepare_tile_effect_texture_space(effectdict, "EffectMountain", "Default")
        LoaderMethods.load_tile_effect_textures(effectdict, "EffectMountain", "Default")
        LoaderMethods.prepare_tile_effect_texture_space(effectdict, "EffectWheat", "Default")
        LoaderMethods.load_tile_effect_textures(effectdict, "EffectWheat", "Default")
        LoaderMethods.prepare_tile_effect_texture_space(effectdict, "EffectTown", "Default")
        LoaderMethods.load_tile_effect_textures(effectdict, "EffectTown", "Default")
        LoaderMethods.prepare_tile_effect_texture_space(effectdict, "EffectRiver", "Default")
        LoaderMethods.load_tile_effect_textures(effectdict, "EffectRiver", "Default", 12)

        # Filenames are built the following way:
        #       <UnitName> + <Orientation> + <AnimationName> + <Framenumber(>=0)> + .png
        # e.g.: UnitSaucer + SW            + Idle            + 0                  + .png
        # => UnitSaucerSWIdle1.png

        # load the files into textures once, then use them all over the game
        # this could take a while, depending on the amount of image data to load

        for previewfilename in PREVIEWS.values():
            #since the same name is used multiple times
            if previewfilename not in Textures.textures["Other"]:
                Textures.textures["Other"][previewfilename] = pygame.image.load(
                    Textures.texturepath + previewfilename
                )
                print("loading preview", Textures.texturepath + previewfilename)

    # Textures have the same name as the texture they point to, without the extension
    # e.g.: UnitSaucerSWIdle

    abilitytexturemapping = {
        0:"MoveAbility.png",
        1:"PunchAbility.png",
        2:"PunchAbility.png",
        3:"PushAbility.png"
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
