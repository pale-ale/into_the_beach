import pygame
import pygame.transform
import pygame.image
import pygame.surface
from ..Enums import PREVIEWS

class Textures:
    """Provides easy access to the textures used in this game."""

    texturepath = "./sprites/"
    textures = {"Units":{}, "Tiles":{}, "Effects":{}, "Other":{}}

    abilitytexturemapping = {
        0:"MoveAbility.png",
        1:"PunchAbility.png",
        2:"PunchAbility.png",
        3:"PushAbility.png"
    }
    backgroundtexturemapping = {
        0:"ProperBackdropWhite.png",
        1:"ProperBackdropBlue.png",
        2:"ProperBackdropRed.png",
        3:"ProperBackdropGreen.png",
        4:"ProperBackdropOrange.png",
    }
    effects = [
        ("EffectFire", "Default", 2),
        ("EffectMountain", "Default", 1),
        ("EffectRiver", "Default", 12),
        ("EffectTown", "Default", 1),
        ("EffectTrees", "Default", 1),
        ("EffectWheat", "Default", 1),
    ]
    tiles = [
        ("TileDirt", "Default"),
        ("TileForest", "Default"),
        ("TileLava", "Default"),
        ("TileRock", "Default"),
    ]

    units = []
    for o in ["ne","se","sw","nw"]:
        units.append(("UnitBase", "Idle", o, 1))
    for o in ["sw"]:
        units.append(("UnitSaucer", "Idle", o, 2))
    for o in ["sw"]:
        units.append(("UnitBloodWraith", "Idle", o, 1))

    @classmethod
    def get_spritesheet(cls, elemtype:str, name:str, animname:str, orientation:str="sw") -> "list[pygame.Surface]":
        """Returns the according spritesheet as a list of images."""
        if elemtype == "Unit":
            return cls.textures["Units"][name][animname][orientation]
        if elemtype == "Tile":
            return cls.textures["Tiles"][name][animname]
        if elemtype == "Effect":
            return cls.textures["Effects"][name][animname]
    
    @staticmethod
    def load_textures(scale:"tuple[float,float]"=(1.0,1.0)):
        """Load the textures from the disk via helpers. Expensive, only use once during startup."""
        unitdict = Textures.textures["Units"]
        for udata in Textures.units:       
            LoaderMethods.prepare_unit_texture_space(unitdict, *udata[:-2])
            LoaderMethods.load_unit_textures(scale, unitdict, *udata)
        
        tiledict = Textures.textures["Tiles"]
        for tdata in Textures.tiles:
            LoaderMethods.prepare_tile_effect_texture_space(tiledict, *tdata)
            LoaderMethods.load_tile_effect_textures(scale, tiledict, *tdata)
        
        effectdict = Textures.textures["Effects"]
        for edata in Textures.effects:
            LoaderMethods.prepare_tile_effect_texture_space(effectdict, *edata[:-1])
            LoaderMethods.load_tile_effect_textures(scale, effectdict, *edata)
       
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


class LoaderMethods():
    """Convenience methods for texture loading."""

    @staticmethod
    def prepare_unit_texture_space(indict:dict, unitname:str, animname:str):
        """Create the needed keys in the dicts if they are not already present."""
        if unitname not in indict.keys():
            indict[unitname] = {}
        if animname not in indict[unitname].keys():
            indict[unitname][animname] = {}
        for orientation in ["ne","se","sw","nw"]:
            if orientation not in indict[unitname][animname].keys():
                indict[unitname][animname][orientation] = []
    
    @staticmethod
    def prepare_tile_effect_texture_space(indict:dict, name:str, animname:str):
        """Create the needed keys in the dicts if they are not already present."""
        if name not in indict.keys():
            indict[name] = {}
        if animname not in indict[name].keys():
            indict[name][animname] = []

    @staticmethod
    def load_unit_textures(scale:"tuple[float,float]", indict:dict, unitname:str, animname:str, orientation:str, framecount:int=1):
        """Load the textures of an animation from the disk."""
        for i in range(framecount):
            path = Textures.texturepath + unitname + orientation.upper() + animname + str(i) + ".png"
            img = LoaderMethods.load_image(path)
            scaledsize = (int(img.get_size()[0]*scale[0]), int(img.get_size()[1]*scale[1]))
            indict[unitname][animname][orientation].append(pygame.transform.scale(img, scaledsize))
   
    @staticmethod
    def load_tile_effect_textures(scale:"tuple[float,float]", indict:dict, name:str, animname:str, framecount:int=1):
        """Load the textures of an animation from the disk."""
        for i in range(framecount):
            path = Textures.texturepath + name + animname + str(i) + ".png"
            img = LoaderMethods.load_image(path)
            scaledsize = (int(img.get_size()[0]*scale[0]), int(img.get_size()[1]*scale[1]))
            indict[name][animname].append(pygame.transform.scale(img, scaledsize))
    
    @staticmethod
    def load_image(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            print("Could not load image at", path)
            return None


