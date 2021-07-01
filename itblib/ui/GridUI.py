from ..gridelements.Effects import EffectBase
from ..gridelements.EffectsUI import EffectBaseUI
from ..gridelements.Tiles import TileBase
from ..gridelements.TilesUI import TileBaseUI
from ..gridelements.Units import UnitBase
from ..gridelements.UnitsUI import UnitBaseUI
from ..Maps import Map
from ..Globals import ClassMapping
from . import IGridObserver
from .. import Grid

import pygame.sprite
import pygame.transform

class GridUI(pygame.sprite.Sprite, IGridObserver.IGridObserver):
    def __init__(self, grid:Grid.Grid):  
        pygame.sprite.Sprite.__init__(self)
        self.grid = grid
        lefttile = self.transform_grid_world(grid.width-1, 0)
        righttile = self.transform_grid_world(0, grid.height-1)
        bottomtile = self.transform_grid_world(grid.width-1, grid.height-1)
        self.width = righttile[0] - lefttile[0] + 64
        self.height = bottomtile[1] + 64
        self.image = pygame.surface.Surface((self.width,self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.uitiles = [TileBaseUI(None) for i in range(grid.width*grid.height)]
        self.uieffects = [EffectBaseUI(None) for i in range(grid.width*grid.height)]
        self.uiunits = [UnitBaseUI(None) for i in range(grid.width*grid.height)]

    def on_add_tile(self, tile):
        x,y = tile.get_position()
        uitile = self.uitiles[self.grid.width*y+x]
        uitile.update_tile(tile)

    def on_add_effect(self, effect):
        x,y = effect.get_position()
        uieffect = self.uieffects[self.grid.width*y+x]
        uieffect.update_effect(effect)
    
    def on_add_unit(self, unit):
        x,y = unit.get_position()
        uiunit = self.uiunits[self.grid.width*y+x]
        uiunit.update_unit(unit)

    def on_move_unit(self, x, y, targetx, targety):
        unit = self.grid.get_unit(targetx,targety)
        self.uiunits[self.grid.width*y+x].update_unit(None)
        self.uiunits[self.grid.width*targety+targetx].update_unit(unit)

    def on_remove_unit(self, x, y):
        self.uiunits[self.grid.c_to_i(x,y)].update_unit(None)
   
    def tick(self, dt:float):
        self.grid.tick(dt)
        self.redraw_grid()
    
    def on_load_map(self, map):
        self.uitiles = [TileBaseUI(None) for i in range(map.width*map.height)]
        self.uieffects = [EffectBaseUI(None) for i in range(map.width*map.height)]
        self.uiunits = [UnitBaseUI(None) for i in range(map.width*map.height)]
    
    def get_unitui(self, x:int, y:int):
        return self.uiunits[self.grid.width*y+x]

    def transform_grid_world(self, gridx:int, gridy:int):
        return (gridx*-32 + gridy*32, gridx*16 + gridy*16)

    def transform_grid_screen(self, gridx:int, gridy:int):
        return (gridx*-32 + gridy*32 + (self.width-64)/2, gridx*16 + gridy*16)

    def draw_group(self, gridgroup):
        for part in gridgroup:
            part.update_image()
            if part.visible:
                part.needsredraw = False
                partx, party = part.get_position()
                screenx,screeny = self.transform_grid_screen(partx, party)
                self.image.blit(part.image, (screenx, screeny), (0,0,64,64))

    def redraw_grid(self):
        self.draw_group(self.uitiles)
        self.draw_group(self.uieffects)
        self.draw_group(self.uiunits)
    
    
