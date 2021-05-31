from EffectsUI import EffectBaseUI
from Effects import EffectBase
from TilesUI import TileBaseUI
from Tiles import TileBase
import pygame.sprite
import pygame.rect
import pygame.image

import Grid

class GridUI(pygame.sprite.Sprite):
    def __init__(self, grid:Grid.Grid, width=1000, height=1000):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.grid = grid
        self.uitiles = [TileBaseUI(None) for i in range(grid.width*grid.height)]
        self.uieffects = [EffectBaseUI(None) for i in range(grid.width*grid.height)]

    def add_tile(self, x:int, y:int, tiletype=TileBase):
        self.grid.add_tile(x, y, tiletype)
        newtile = self.grid.get_tile(x,y)
        uitile = self.uitiles[self.grid.width*y+x]
        uitile.update_tile(newtile)
        uitile.visible = True
   
    def add_effect(self, x:int, y:int, effecttype=EffectBase):
        self.grid.add_effect(x, y, effecttype)
        neweffect = self.grid.get_effect(x,y)
        uieffect = self.uieffects[self.grid.width*y+x]
        uieffect.update_effect(neweffect)
        uieffect.visible = True
        
    def tick(self, dt:float):
        self.grid.tick(dt)
        self.redraw_grid()

    def transform_grid_screen(self, gridx:int, gridy:int):
        return (gridx*-32 + gridy*32, gridx*16 + gridy*16)

    def draw_group(self, gridgroup):
        for part in gridgroup:
            part.update()
            if part.visible:
                partx, party = part.get_position()
                screenx,screeny = self.transform_grid_screen(partx, party)
                self.image.blit(part.image, 
                    (
                    screenx+self.width*.5-32, 
                    screeny+self.height*.5-self.grid.height*16
                    )
                )

    def redraw_grid(self):
        self.draw_group(self.uitiles)
        self.draw_group(self.uieffects)
