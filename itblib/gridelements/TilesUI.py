from ..ui.TextureManager import Textures
from .GridElementUI import GridElementUI
from .Tiles import TileBase

class TileBaseUI(GridElementUI):
    def __init__(self, tile:TileBase, width:int=64, height:int=64):
        super().__init__(width=width, height=height, parentelement=tile) 

    def update_tile(self, newtile:TileBase):
        self._parentelement = newtile
        self.visible = bool(newtile)
        if self._parentelement:
            self.update_texture_source(
                Textures.get_spritesheet("Tile", newtile.name, "Default")
            )
