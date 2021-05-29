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

    def tick(self, dt:float):
        self.grid.tick(dt)
        self.redraw_grid()

    def draw_group(self, gridgroup, mapping):
        for part in gridgroup:
            if part:
                texture = pygame.image.load(Tex.texturepath + mapping[part.id])
                partx, party = part.pos
                screenx,screeny = (partx*-32 + party*32, partx*16 + party*16)
                self.image.blit(texture, 
                    (
                    screenx+self.width*.5-32, 
                    screeny+self.height*.5-self.grid.height*16
                    )
                )
    def redraw_grid(self):
        self.draw_group(self.grid.tiles, Tex.tilemapping)
        self.draw_group(self.grid.effects, Tex.effectmapping)