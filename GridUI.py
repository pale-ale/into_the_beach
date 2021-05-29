from pygame import surface
import pygame.sprite
import pygame.rect
import pygame.image

import Grid
from Globals import Textures as Tex

from typing import cast

class GridUI(pygame.sprite.Sprite):
    def __init__(self, grid:Grid.Grid, width=1000, height=700):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.grid = grid

    def redraw_grid(self):
        for tile in self.grid.tiles:
            if tile:
                assert isinstance(tile, Grid.TileBase)
                tile = cast(Grid.TileBase, tile)
                assert tile.id in Tex.mappings.keys()
                texture = pygame.image.load(Tex.texturepath + Tex.mappings[tile.id])
                tilex, tiley = tile.pos
                screenx,screeny = (tilex*-32 + tiley*32, tilex*16 + tiley*16)
                self.image.blit(texture, 
                    (
                    screenx+self.width*.5-32, 
                    screeny+self.height*.5-self.grid.height*16
                    )
                )
       
    