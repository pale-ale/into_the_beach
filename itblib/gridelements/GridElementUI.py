from itblib.gridelements.GridElement import GridElement
from itblib.ui.TextureManager import Textures
from itblib.ui.animations.MultiSprite import MultiSprite

class GridElementUI(MultiSprite):
    """Graphical representation of a GridElement."""
    
    def __init__(self, parentelement:GridElement, direction:"str|None", width:int=64, height:int=64, framespeed:float=.5):
        texturekey = parentelement.name
        if direction:
            texturekey += direction + "Idle"
        else:
            texturekey += "Default"
        spritesheet = Textures.get_spritesheet(texturekey)
        super().__init__(spritesheet, width=width, height=height, frametime=framespeed, playing=True)
        self.visible = True
        self.needsredraw = True
        self._parentelement = parentelement
        self.direction = direction
