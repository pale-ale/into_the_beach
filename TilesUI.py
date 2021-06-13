import pygame.sprite

from Globals import Textures
from GridElementUI import GridElementUI
from Tiles import TileBase

class TileBaseUI(GridElementUI):
    def __init__(self, tile:TileBase, width:int=64, height:int=64):
        super().__init__() 
        self.visible = bool(tile)
        self._tile = tile
        self._textures = []

    def update_texture_source(self):
        self._textures.clear()
        if self._tile:
            self._textures = Textures.get_tile_effect_spritesheet(True, self._tile.name, "Default")
        self.needsredraw = True

    def update_tile(self, newtile):
        self._tile = newtile
        self.update_texture_source()

    def update(self):
        if self.visible:
            self.image = self._textures[int(self._tile.age % len(self._textures))]
    
    def get_position(self):
        return self._tile.get_position()
