import pygame.sprite

from TextureManager import Textures
from GridElementUI import GridElementUI
from Tiles import TileBase
from pygame.display import update

class TileBaseUI(GridElementUI):
    def __init__(self, tile:TileBase, width:int=64, height:int=64):
        super().__init__(parentelement=tile) 

    def update_tile(self, newtile):
        self._parentelement = newtile
        self.visible = bool(newtile)
        if self._parentelement:
            self.update_texture_source(
                Textures.get_spritesheet("Tile", newtile.name, "Default")
            )

    def get_position(self):
        return self._parentelement.get_position()
