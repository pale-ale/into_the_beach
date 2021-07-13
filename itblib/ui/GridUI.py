from itblib.gridelements.GridElementUI import GridElementUI
from ..gridelements.Effects import EffectBase
from ..gridelements.EffectsUI import EffectBaseUI, EffectRiverUI
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
    """The Graphical representation of the grid."""

    def __init__(self, grid:Grid.Grid):  
        pygame.sprite.Sprite.__init__(self)
        self.grid = grid
        lefttile = self.transform_grid_world((grid.width-1, 0))
        righttile = self.transform_grid_world((0, grid.height-1))
        bottomtile = self.transform_grid_world((grid.width-1, grid.height-1))
        self.width = righttile[0] - lefttile[0] + 64
        self.height = bottomtile[1] + 64
        self.image = pygame.surface.Surface((self.width,self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.uitiles = [TileBaseUI(None) for i in range(grid.width*grid.height)]
        self.uieffects = [EffectBaseUI(None) for i in range(grid.width*grid.height)]
        self.uiunits = [UnitBaseUI(None) for i in range(grid.width*grid.height)]

    def on_add_tile(self, tile:TileBase):
        """Add the UI version of the new tile added to the normal grid."""
        uitile = self.uitiles[self.grid.c_to_i(tile.pos)]
        uitile.update_tile(tile)

    def on_add_effect(self, effect:EffectBase):
        """Add the UI version of the new effect added to the normal grid."""
        gridindex = self.grid.c_to_i(effect.pos)
        if effect and type(effect).__name__ == "EffectRiver":
            self.uieffects[gridindex] = EffectRiverUI(None)
        uieffect = self.uieffects[gridindex]
        uieffect.update_effect(effect)
    
    def on_add_unit(self, unit:UnitBase):
        """Add the UI version of the new unit added to the normal grid."""
        uiunit = self.uiunits[self.grid.c_to_i(unit.pos)]
        uiunit.update_unit(unit)

    def on_move_unit(self, from_pos:"tuple[int,int]", to_pos:"tuple[int,int]"):
        """Move the UI version of the moved unit from the normal grid."""
        unit = self.grid.get_unit(to_pos)
        self.uiunits[self.grid.c_to_i(from_pos)].update_unit(None)
        self.uiunits[self.grid.c_to_i(to_pos)].update_unit(unit)

    def on_remove_unit(self, x:int, y:int):
        """Remove a UI-unit at the given position."""
        self.uiunits[self.grid.c_to_i(x,y)].update_unit(None)
   
    def tick(self, dt:float):
        """Update the graphics and animations' frames."""
        self.grid.tick(dt)
        self.redraw_grid()
    
    def on_load_map(self, map:Map):
        """Clear all the residual graphic objects, as they will be added during map load."""
        self.uitiles = [TileBaseUI(None) for i in range(map.width*map.height)]
        self.uieffects = [EffectBaseUI(None) for i in range(map.width*map.height)]
        self.uiunits = [UnitBaseUI(None) for i in range(map.width*map.height)]
    
    def get_unitui(self, pos:"tuple[int,int]"):
        """Return the UI-unit at given position."""
        return self.uiunits[self.grid.c_to_i(pos)]

    def transform_grid_world(self, gridpos:"tuple[int,int]"):
        """Return the world position of a given grid coordinate."""
        return (gridpos[0]*-32 + gridpos[1]*32, gridpos[0]*16 + gridpos[1]*16)

    def transform_grid_screen(self, gridpos:"tuple[int,int]"):
        """Return the screen position of a given grid coordinate."""
        return (int(gridpos[0]*-32 + gridpos[1]*32 + (self.width-64)/2), gridpos[0]*16 + gridpos[1]*16)

    def draw_group(self, gridgroup:"list[GridElementUI]"):
        """Draw the groups' images into the internal image."""
        for part in gridgroup:
            part.update_image()
            if part.visible:
                part.needsredraw = False
                screenx,screeny = self.transform_grid_screen(part._parentelement.pos)
                self.image.blit(part.image, (screenx, screeny), (0,0,64,64))

    def redraw_grid(self):
        """Redraw every group."""
        self.draw_group(self.uitiles)
        self.draw_group(self.uieffects)
        self.draw_group(self.uiunits)
    
    
