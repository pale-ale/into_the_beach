from typing import Optional

import pygame
import pygame.image
import pygame.surface
import pygame.transform
from itblib.globals.Constants import PREVIEWS

TEXTURE_PATHS = [
    "units",
    "tiles",
    "tile_effects",
    "ability_previews",
    "effect_icons",
    "ability_icons",
    ""
]

class ETEXTURETYPE:
    UNIT = 0
    TILE = 1
    TILE_EFFECT = 2
    ABILITY_PREVIEW = 3
    EFFECT_ICON = 4
    ABILITY_ICON = 5
    OTHER = 6


class Textures:
    """Provides easy access to the textures used in this game."""

    texturepath = "./sprites/"
    _textures:"dict[str,list]" = {}

    abilitytexturemapping = {
        0:"MovementAbility",
        1:"PunchAbility",
        2:"PunchAbility",
        3:"PushAbility",
        4:"ObjectiveAbility",
        5:"HealAbility",
        6:"BurrowAbility",
        7:"DreadfulNoiseAbility"
    }
    
    texturekeys:list[tuple[int,str,str, Optional[int]]] = [
        (ETEXTURETYPE.TILE_EFFECT,  "Mountain"     , "Default",  1),
        (ETEXTURETYPE.TILE_EFFECT,  "River"        , "Default",  6),
        (ETEXTURETYPE.TILE_EFFECT,  "Town"         , "Default",  1),
        (ETEXTURETYPE.TILE_EFFECT,  "Wheat"        , "Default",  1),
        (ETEXTURETYPE.TILE_EFFECT,  "Heal"         , "Default", 10),
        (ETEXTURETYPE.TILE_EFFECT,  "StartingArea" , "Default",  1),

        (ETEXTURETYPE.TILE, "Dirt" , "Default", 1),
        (ETEXTURETYPE.TILE, "Water", "Default", 1),
        (ETEXTURETYPE.TILE, "Lava" , "Default", 2),
        (ETEXTURETYPE.TILE, "Rock" , "Default", 1),

        (ETEXTURETYPE.UNIT, "Saucer"        , "SWIdle"    ,  1),
        (ETEXTURETYPE.UNIT, "BloodWraith"   , "SWIdle"    ,  1),
        (ETEXTURETYPE.UNIT, "Homebase"      , "SWIdle"    ,  4),
        (ETEXTURETYPE.UNIT, "Knight"        , "SWIdle"    ,  5),
        (ETEXTURETYPE.UNIT, "Burrower"      , "SWIdle"    ,  1),
        (ETEXTURETYPE.UNIT, "Burrower"      , "SWBurrowed", 10),
        (ETEXTURETYPE.UNIT, "SirenHead"     , "SWIdle"    ,  1),
        (ETEXTURETYPE.UNIT, "Chipmonk"      , "SWIdle"    ,  1),

        (ETEXTURETYPE.EFFECT_ICON, "Bleeding"       , ""   ,  None),
        (ETEXTURETYPE.EFFECT_ICON, "Burrowed"       , ""   ,  None),
        (ETEXTURETYPE.EFFECT_ICON, "DreadfulNoise"  , ""   ,  None),
        (ETEXTURETYPE.EFFECT_ICON, "Ablaze"         , ""   ,  None),
        (ETEXTURETYPE.EFFECT_ICON, "Mountain"       , ""   ,  None),
        (ETEXTURETYPE.EFFECT_ICON, "Wheat"          , ""   ,  None),

        (ETEXTURETYPE.OTHER, "Cursor"       , "", 1)
    ]
    """[(<ETEXTURETYPE>, <effect_name>, <anim_name>, <frame_count>), ...]"""

    for ability_name in abilitytexturemapping.values():
        texturekeys.append((ETEXTURETYPE.ABILITY_ICON, ability_name, "", None))
      
    ability_preview_names = {tuple(prevval.split(':')) for prevval in PREVIEWS.values() if ':' in prevval}
    for ability_name, preview_name in ability_preview_names:
        texturekeys.append((ETEXTURETYPE.ABILITY_PREVIEW, ability_name, preview_name, 1))

    for o in ["NE","SE","SW","NW"]:
        texturekeys.append((ETEXTURETYPE.UNIT, "Base", o + "Idle", 1))

    @classmethod
    def get_spritesheet(cls, key:str) -> "list[pygame.Surface]|None":
        """Returns the according spritesheet as a list of images or None if it it doesn't exist"""
        if key in cls._textures:
            return cls._textures[key]
        print(f"Texturemanager: Key '{key}' not found.")
        return None
    
    @staticmethod
    def load_textures(scale:"tuple[float,float]"=(1.0,1.0)):
        """Load the textures from the disk via helpers. Expensive, only use once during startup."""
        for effect_info in Textures.texturekeys:
            key = "".join(effect_info[1:-1])
            LoaderMethods.prepare_texture_space(key)
            LoaderMethods.load_textures(scale, key, *effect_info)

        # for data in Textures.texturekeys:
        #     if len(data) > 1:
        #         key = "".join(data[:-1])
        #         LoaderMethods.prepare_texture_space(key)
        #         LoaderMethods.load_textures(scale, key, data[-1])
        #     else:
        #         key = str(data[0])
        #         LoaderMethods.prepare_texture_space(key)
        #         LoaderMethods.load_textures(scale, key, None)

       
        # Filenames are built the following way:
        #       <UnitName> + <Orientation> + <AnimationName> + <Framenumber(>=0)> + .png
        # e.g.: UnitSaucer + SW            + Idle            + 0                  + .png
        # => UnitSaucerSWIdle1.png

        # load the files into textures once, then use them all over the game
        # this could take a while, depending on the amount of image data to load

        # for previewfilename in PREVIEWS.values():
        #     #since the same name is used multiple times
        #     if previewfilename not in Textures.textures["Other"]:
        #         Textures.textures["Other"][previewfilename] = pygame.image.load(
        #             Textures.texturepath + previewfilename
        #         )


class LoaderMethods():
    """Convenience methods for texture loading."""

    @staticmethod
    def prepare_texture_space(key:str):
        """Create the needed keys if they are not already present."""
        texs = Textures._textures
        if key not in texs.keys():
            texs[key] = []

    @staticmethod
    def load_textures(scale:"tuple[float,float]", key:str, texturetype:int, name:str, animname:str, framecount:Optional[int]):
        """Load the textures of an animation from the disk."""
        if framecount is not None:
            for i in range(1,framecount+1):
                path = f"{Textures.texturepath}/{TEXTURE_PATHS[texturetype]}/{name}/{animname}{str(i)}.png"
                img = LoaderMethods.load_image(path)
                if img:
                    scaledsize = (int(img.get_size()[0]*scale[0]), int(img.get_size()[1]*scale[1]))
                    Textures._textures[key].append(pygame.transform.scale(img, scaledsize).convert_alpha())
        else:
            path = f"{Textures.texturepath}/{TEXTURE_PATHS[texturetype]}/{name}.png"
            img = LoaderMethods.load_image(path)
            if img:
                scaledsize = (int(img.get_size()[0]*scale[0]), int(img.get_size()[1]*scale[1]))
                Textures._textures[key].append(pygame.transform.scale(img, scaledsize).convert_alpha())

    @staticmethod
    def load_image(path):
        try:
            img = pygame.image.load(path)
        except:
            print("Could not load image at", path)
            return None
        return img.convert_alpha()


