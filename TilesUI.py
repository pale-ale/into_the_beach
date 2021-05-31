import pygame.sprite
import pygame.rect
import pygame.image

from Tiles import TileBase
from Globals import Textures

class TileBaseUI(pygame.sprite.Sprite):
    def __init__(self, tile:TileBase, width:int=64, height:int=64):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((100,100,100))
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.visible = bool(tile)
        self._tile = tile
        self._textures = []                

    def update_texture_source(self):
        self._textures.clear()
        if self._tile:
            path_suffixes = Textures.tilemapping[self._tile.id]
            for path_suffix in path_suffixes:
                self._textures.append(pygame.image.load(Textures.texturepath + path_suffix))

    def update_tile(self, newtile):
        self._tile = newtile
        self.update_texture_source()

    def update(self):
        if self.visible:
            self.image = self._textures[int(self._tile.age % len(self._textures))]
    
    def get_position(self):
        return self._tile.get_position()