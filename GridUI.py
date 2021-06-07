from Effects import EffectBase
from EffectsUI import EffectBaseUI
from Tiles import TileBase
from TilesUI import TileBaseUI
from Units import UnitBase
from UnitsUI import UnitBaseUI
from Maps import Map
from Globals import Classes

import pygame.sprite
import pygame.transform
import IGridObserver
import Grid

class GridUI(pygame.sprite.Sprite, IGridObserver.IGridObserver):
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

    def on_add_tile(self, tile):
        x,y = tile.get_position()
        uitile = self.uitiles[self.grid.width*y+x]
        uitile.update_tile(tile)
        uitile.visible = True

    def on_add_effect(self, effect):
        x,y = effect.get_position()
        uieffect = self.uieffects[self.grid.width*y+x]
        uieffect.update_effect(effect)
        uieffect.visible = True
    
    def on_add_unit(self, unit):
        x,y = unit.get_position()
        uiunit = self.uiunits[self.grid.width*y+x]
        uiunit.update_unit(unit)
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
