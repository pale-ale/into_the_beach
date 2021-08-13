from typing import Optional
import pygame
import pygame.transform
import pygame.image
import pygame.surface
from ..Enums import PREVIEWS

class Textures:
    """Provides easy access to the textures used in this game."""

    texturepath = "./sprites/"
    textures:"dict[str,list]" = {}

    abilitytexturemapping = {
        0:"MoveAbility",
        1:"PunchAbility",
        2:"PunchAbility",
        3:"PushAbility",
        4:"ObjectiveAbility",
        5:"HealAbility",
    }
    backgroundtexturemapping = {
        0:"ProperBackdropWhite",
        1:"ProperBackdropBlue",
        2:"ProperBackdropRed",
        3:"ProperBackdropGreen",
        4:"ProperBackdropOrange",
    }
    texturekeys = [
        ("EffectFire", "Default", 2),
        ("EffectMountain", "Default", 1),
        ("EffectRiver", "Default", 6),
        ("EffectTown", "Default", 1),
        ("EffectTrees", "Default", 1),
        ("EffectWheat", "Default", 1),
        ("EffectHeal", "Default", 10),

        ("TileDirt", "Default", 1),
        ("TileWater", "Default", 1),
        ("TileLava", "Default", 1),
        ("TileRock", "Default", 1),
    ]
    for p in PREVIEWS.values():
        texturekeys.append((p, 1))
    for p in abilitytexturemapping.values():
        texturekeys.append((p,))
    for p in backgroundtexturemapping.values():
        texturekeys.append((p,))

    for o in ["NE","SE","SW","NW"]:
        texturekeys.append(("UnitBase", o, "Idle", 1))
    for o in ["SW"]:
        texturekeys.append(("UnitSaucer", o, "Idle", 2))
    for o in ["SW"]:
        texturekeys.append(("UnitBloodWraith", o, "Idle", 1))
    for o in ["SW"]:
        texturekeys.append(("UnitCrystal", o, "Idle", 4))

    @classmethod
    def get_spritesheet(cls, key:str) -> "list[pygame.Surface]":
        """Returns the according spritesheet as a list of images."""
        return cls.textures[key]
    
    @staticmethod
    def load_textures(scale:"tuple[float,float]"=(1.0,1.0)):
        """Load the textures from the disk via helpers. Expensive, only use once during startup."""
        for data in Textures.texturekeys:
            if len(data) > 1:
                key = "".join(data[:-1])
                LoaderMethods.prepare_texture_space(key)
                LoaderMethods.load_textures(scale, key, data[-1])
            else:
                key = str(data[0])
                LoaderMethods.prepare_texture_space(key)
                LoaderMethods.load_textures(scale, key, None)

       
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
        texs = Textures.textures
        if key not in texs.keys():
            texs[key] = []

    @staticmethod
    def load_textures(scale:"tuple[float,float]", key:str, framecount:"Optional[int]"):
        """Load the textures of an animation from the disk."""
        if framecount is not None:
            for i in range(framecount):
                path = Textures.texturepath + key + str(i+1) + ".png"
                img = LoaderMethods.load_image(path)
                scaledsize = (int(img.get_size()[0]*scale[0]), int(img.get_size()[1]*scale[1]))
                Textures.textures[key].append(pygame.transform.scale(img, scaledsize))
        else:
            path = Textures.texturepath + key + ".png"
            img = LoaderMethods.load_image(path)
            scaledsize = (int(img.get_size()[0]*scale[0]), int(img.get_size()[1]*scale[1]))
            Textures.textures[key].append(pygame.transform.scale(img, scaledsize))

   
    @staticmethod
    def load_image(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            print("Could not load image at", path)
            return None


