from itblib.gridelements.GridElement import GridElement
from itblib.ui.animations import FlipbookAnimation
from itblib.ui.TextureManager import Textures


class GridElementUI(FlipbookAnimation):
    """Graphical representation of a GridElement."""

    def __init__(self, parentelement:GridElement, direction:"str|None", framespeed:float=.5):
        texturekey = parentelement.name
        if direction:
            texturekey += direction + "Idle"
        else:
            texturekey += "Default"
        spritesheet = Textures.get_spritesheet(texturekey)
        FlipbookAnimation.__init__(self, spritesheet, frametime=framespeed, running=True, looping=True)
        self._parentelement = parentelement
        self.direction = direction
    