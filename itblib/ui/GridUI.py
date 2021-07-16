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
        self.standard_tilesize = (64,64)
        self.tilesize = self.standard_tilesize
        self.grid = grid
        lefttile = self.transform_grid_world((grid.width-1, 0))
        righttile = self.transform_grid_world((0, grid.height-1))
        bottomtile = self.transform_grid_world((grid.width-1, grid.height-1))
        self.width = righttile[0] - lefttile[0] + self.tilesize[0]
        self.height = bottomtile[1] + self.tilesize[1]/2
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
    
    def reload_from_grid(self):
        """Reload everything from the grid. Useful to update e.g. graphic scale."""
        g = self.grid
        self.clear_map()
        for unitdata in g.units:
            if unitdata:
                self.on_add_unit(unitdata)
        for tiledata in g.tiles:
            if tiledata:
                self.on_add_tile(tiledata)
        for effectdata in g.effects:
            if effectdata:
                self.on_add_effect(effectdata)

    def clear_map(self):
        """Sets every graphic's data source to 'None'."""
        self.uitiles = [TileBaseUI(None) for i in self.uitiles]
        self.uieffects = [EffectBaseUI(None) for i in self.uieffects]
        self.uiunits = [UnitBaseUI(None) for i in self.uiunits]
    
    def on_load_map(self, map:Map):
        """Clear all the residual graphic objects, as they will be added during map load."""
        self.clear_map()
    
    def get_unitui(self, pos:"tuple[int,int]"):
        """Return the UI-unit at given position."""
        return self.uiunits[self.grid.c_to_i(pos)]

    def transform_grid_world(self, gridpos:"tuple[int,int]"):
        """Return the world position of a given grid coordinate."""
        return (int(gridpos[0]*-self.tilesize[0]/2 + gridpos[1]*self.tilesize[0]/2), 
                int(gridpos[0]*self.tilesize[1]/4 + gridpos[1]*self.tilesize[1]/4))

    def transform_grid_screen(self, gridpos:"tuple[int,int]"):
        """Return the screen position of a given grid coordinate."""
        gw = self.transform_grid_world(gridpos)
        return (int(gw[0] + (self.width-self.tilesize[0])/2), gw[1])

    def draw_group(self, gridgroup:"list[GridElementUI]", offset:"tuple[int,int]"=(0,0)):
        """Draw the groups' images into the internal image."""
        for part in gridgroup:
            part.update_image()
            if part.visible:
                part.needsredraw = False
                x, y = self.transform_grid_screen(part._parentelement.pos)
                x, y = x+offset[0], y+offset[1]
                self.image.blit(part.image, (x,y), (0,0,*self.tilesize))

    def redraw_grid(self):
        """Redraw every group."""
        self.draw_group(self.uitiles)
        self.draw_group(self.uieffects)
        self.draw_group(self.uiunits,(0,-20))
    
    def update_displayscale(self, newscale:"tuple[float,float]", newsize):
        print("updating scale to", newscale)
        self.tilesize = (self.standard_tilesize[0] * newscale[0],
                         self.standard_tilesize[1] * newscale[1])
        self.image.fill((0,0,0,0))
        self.reload_from_grid()
        

    
    
