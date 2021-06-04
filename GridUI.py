from Effects import EffectBase
from EffectsUI import EffectBaseUI
from Tiles import TileBase
from TilesUI import TileBaseUI
from Units import UnitBase
from UnitsUI import UnitBaseUI

import pygame.sprite
import pygame.transform

import Grid

class GridUI(pygame.sprite.Sprite):
    def __init__(self, grid:Grid.Grid):  
        pygame.sprite.Sprite.__init__(self)
        self.grid = grid
        lefttile = self.transform_grid_screen(grid.width-1, 0)
        righttile = self.transform_grid_screen(0, grid.height-1)
        bottomtile = self.transform_grid_screen(grid.width-1, grid.height-1)
        self.width = righttile[0] - lefttile[0]
        self.height = bottomtile[1]
        self.image = pygame.surface.Surface((self.width+64,self.height+64), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.uitiles = [TileBaseUI(None) for i in range(grid.width*grid.height)]
        self.uieffects = [EffectBaseUI(None) for i in range(grid.width*grid.height)]
        self.uiunits = [UnitBaseUI(None) for i in range(grid.width*grid.height)]

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
    
    def add_unit(self, x:int, y:int, unittype=UnitBase):
        self.grid.add_unit(x, y, unittype)
        newunit = self.grid.get_unit(x,y)
        uiunit = self.uiunits[self.grid.width*y+x]
        uiunit.update_unit(newunit)
        uiunit.visible = True
   
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
                self.image.blit(part.image, (screenx+self.width*.5, screeny), (0,0,64,64))
                part.needsredraw = False

    def redraw_grid(self):
        self.draw_group(self.uitiles)
        self.draw_group(self.uieffects)
        self.draw_group(self.uiunits)
