from pygame import Rect, draw
from itblib.net.NetEvents import NetEvents 
from ..gridelements.Effects import EffectBase
from ..gridelements.EffectsUI import EffectBaseUI, EffectHealUI, EffectRiverUI
from ..gridelements.Tiles import TileBase
from ..gridelements.TilesUI import TileBaseUI
from ..gridelements.Units import UnitBase
from ..gridelements.UnitsUI import UnitBaseUI
from ..Maps import Map
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
        self.uitiles:"list[TileBaseUI|None]" = [None]*grid.width*grid.height
        self.uieffects:"list[list[EffectBaseUI]]" = [[] for i in range(grid.width*grid.height)]
        self.uiunits:"list[UnitBaseUI|None]" = [None]*grid.width*grid.height
        self.tilesprites = pygame.sprite.Group()
        self.effectsprites = pygame.sprite.Group()
        self.unitsprites = pygame.sprite.Group()
        self.unitdrawoffset = -20

    def on_add_tile(self, tile:TileBase):
        """Add the UI version of the new tile added to the normal grid."""
        uitile = TileBaseUI(tile)
        uitile.rect = Rect(*self.transform_grid_screen(tile.pos), 64, 64)
        self.uitiles[self.grid.c_to_i(tile.pos)] = uitile
        self.tilesprites.add(uitile)

    def on_add_unit(self, unit:UnitBase):
        """Add the UI version of the new unit added to the normal grid."""
        uiunit = UnitBaseUI(unit) 
        x, y = self.transform_grid_screen(unit.pos)
        uiunit.rect = Rect(x, y + self.unitdrawoffset, 64, 64)
        self.uiunits[self.grid.c_to_i(unit.pos)] = uiunit
        self.unitsprites.add(uiunit)
    
    def on_add_effect(self, effect:EffectBase):
        """Add the UI version of the new effect added to the normal grid."""
        assert isinstance(effect, EffectBase)
        gridindex = self.grid.c_to_i(effect.pos)
        if type(effect).__name__ == "EffectRiver":
            uieffect = EffectRiverUI(effect)
        elif type(effect).__name__ == "EffectHeal":
            uieffect = EffectHealUI(effect)
        else:
            uieffect = EffectBaseUI(effect)
        self.uieffects[gridindex].append(uieffect)
        uieffect.rect = Rect(*self.transform_grid_screen(effect.pos), 64, 64)
        self.effectsprites.add(uieffect)

    def on_move_unit(self, from_pos:"tuple[int,int]", to_pos:"tuple[int,int]"):
        """Move the UI version of the moved unit from the normal grid."""
        print("GridUI: Moving unit from", from_pos, "to", to_pos)
        uiunit = self.uiunits[self.grid.c_to_i(from_pos)]
        x, y = self.transform_grid_screen(to_pos)
        uiunit.rect = Rect(x, y + self.unitdrawoffset, 64, 64)
        self.uiunits[self.grid.c_to_i(from_pos)] = None
        self.uiunits[self.grid.c_to_i(to_pos)] = uiunit
    
    def on_remove_unit(self, pos:"tuple[int,int]"):
        """Remove a UI-unit at the given position."""
        self.uiunits[self.grid.c_to_i(pos)] = None
   
    def on_remove_effect(self, effect:"EffectBase", pos:"tuple[int,int]"):
        """Remove a UI-effect at the given position."""
        for uieffect in self.uieffects[self.grid.c_to_i(pos)][:]:
            if uieffect._parentelement == effect:
                self.effectsprites.remove(uieffect)
                self.uieffects[self.grid.c_to_i(pos)].remove(uieffect)
                return
   
    def update(self):
        """Update the graphics and animations' frames."""
        self.tilesprites.update()
        self.effectsprites.update()
        self.unitsprites.update()
        self.redraw_grid_2()

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
        c = self.grid.width*self.grid.height
        self.uitiles:"list[TileBaseUI|None]" = [None]*c
        self.uieffects:"list[list[EffectBaseUI]]" = [[] for i in range(c)]
        self.uiunits:"list[UnitBaseUI|None]" = [None]*c
    
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

    def redraw_grid_2(self):
        """Redraw every group."""
        self.image.fill((0))
        self.tilesprites.draw(self.image)
        self.effectsprites.draw(self.image)
        for uiunit in self.uiunits:
            if uiunit and uiunit.visible:
                c = uiunit.rect.center
                o = 3
                squaresize = 48
                l = (c[0] - int(squaresize/2) , c[1] + o)
                r = (c[0] + int(squaresize/2) , c[1] + o)
                t = (c[0], c[1] - int(squaresize/4) + o)
                b = (c[0], c[1] + int(squaresize/4) + o)
                draw.lines(self.image, NetEvents.session._players[uiunit._parentelement.ownerid].color, True, (l, t, r, b), 1)
        self.unitsprites.draw(self.image)
