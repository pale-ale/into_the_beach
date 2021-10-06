from itblib.gridelements.GridElement import GridElement
from itblib.ui.TextureManager import Textures
from itblib.ui.animations.MultiSprite import MultiSprite
import pygame

class GridElementUI(MultiSprite):
    """Graphical representation of a GridElement."""
    
    def __init__(self, parentelement:GridElement, direction:"str|None", width:int=64, height:int=64, framespeed:float=.5):
        assert isinstance(parentelement, GridElement), "GridElementUIs must now have an associated parent."
        texturekey = parentelement.name
        if direction:
            texturekey += direction + "Idle"
        else:
            texturekey += "Default"
        spritesheet = Textures.get_spritesheet(texturekey)
        super().__init__(spritesheet, width=width, height=height, frametime=framespeed)
        self.visible = True
        self.needsredraw = True
        self._parentelement = parentelement
        self.direction = direction
        self.update_texture_source(spritesheet)

    def update_texture_source(self, source:"list[pygame.Surface]"):
        """Set a new spritesheet as this UIElements' texture soure."""
        assert len(source) > 0, self._parentelement.name + " has not received a texture"
        self._textures = source
        self.needsredraw = True
        self.animframe = -1
        self.frametime = 0
