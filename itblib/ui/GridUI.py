from typing import Generator

import pygame
from itblib.globals.Constants import STANDARD_TILE_SIZE, STANDARD_UNIT_SIZE
from itblib.globals.GridElementUIFactory import GridElementUIFactory
from itblib.gridelements.GridElementUI import GridElementUI
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.ui.PerfSprite import PerfSprite
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.Vec import add

from ..Grid import Grid
from ..gridelements.Effects import EffectBase
from ..gridelements.EffectsUI import EffectBaseUI
from ..gridelements.Tiles import TileBase
from ..gridelements.TilesUI import TileBaseUI
from ..gridelements.UnitsUI import UnitBaseUI
from ..Maps import Map
from . import IGridObserver


class GridUI(PerfSprite, ComponentAcceptor, IGridObserver.IGridObserver):
    """The Graphical representation of the grid."""
    def __init__(self, grid:Grid):  
        PerfSprite.__init__(self)
        ComponentAcceptor.__init__(self)
        self.tfc = TransformComponent()
        self.tfc.attach_component(self)
        self.grid = grid
        self.tile_size = STANDARD_TILE_SIZE
        left_tile = self.transform_grid_world((grid.size[0]-1, 0))
        right_tile = self.transform_grid_world((0, grid.size[1]-1))
        bottom_tile = self.transform_grid_world((grid.size[0]-1, grid.size[1]-1))
        self.width = right_tile[0] - left_tile[0] + self.tile_size[0]
        self.height = bottom_tile[1] + self.tile_size[1]
        self.board_size = (self.width, self.height)
        self.ui_tiles:"list[TileBaseUI|None]" = [None]*grid.size[0]*grid.size[1]
        self.ui_worldeffects:"list[list[EffectBaseUI]]" = [[] for i in range(grid.size[0]*grid.size[1])]
        self.ui_units:"list[UnitBaseUI|None]" = [None]*grid.size[0]*grid.size[1]
        self.ui_unit_effects:"list[list[EffectBaseUI]]" = [[] for i in range(grid.size[0]*grid.size[1])]
        self.unit_draw_offset = (0,-10)
        self.pan = (96,0)
        self.phase_change_callback = None
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
        # self.mid_blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
        # self.post_blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
     
    def on_change_phase(self, phase: int):
        if phase == 2:
            self._add_get_clear_blit()
        if self.phase_change_callback:
            self.phase_change_callback(phase)

    def on_add_tile(self, tile:TileBase):
        """Add the UI version of the new tile added to the normal grid."""
        ui_tile_class = GridElementUIFactory.find_tile_class(type(tile).__name__ + "UI")
        if ui_tile_class:
            ui_tile = ui_tile_class(tile,  pygame.Rect(*self.transform_grid_screen(tile.pos), 64, 96))
            self.ui_tiles[self.grid.c_to_i(tile.pos)] = ui_tile
            self.add_gridui_element(ui_tile)
    
    def update_pan(self, newpan:"tuple[int,int]"):
        self._add_get_clear_blit()
        self.pan = newpan
        self.tfc.relative_position = newpan
    
    def add_gridui_element(self, elem:GridElementUI):
        elem_tfc:TransformComponent = elem.get_component(TransformComponent)
        if elem_tfc:
            elem_tfc.set_transform_target(self)

    def on_add_unit(self, unit:UnitBase):
        """Add the UI version of the new unit added to the normal grid."""
        ui_unit_class = GridElementUIFactory.find_unit_class(type(unit).__name__ + "UI")
        if ui_unit_class:   
            ui_unit = ui_unit_class(unit, pygame.Rect(*add(self.unit_draw_offset, self.transform_grid_screen(unit.pos)), *STANDARD_UNIT_SIZE))
            self.ui_units[self.grid.c_to_i(unit.pos)] = ui_unit
            self.add_gridui_element(ui_unit)
    
    def on_add_worldeffect(self, effect:EffectBase):
        """Add the UI version of the new effect added to the normal grid."""
        gridindex = self.grid.c_to_i(effect.pos)
        ui_worldeffect_class = GridElementUIFactory.find_effect_class(type(effect).__name__ + "UI")
        if ui_worldeffect_class:
            ui_worldeffect = ui_worldeffect_class(effect, pygame.Rect(*self.transform_grid_screen(effect.pos), *STANDARD_UNIT_SIZE))
            self.ui_worldeffects[gridindex].append(ui_worldeffect)
            self.add_gridui_element(ui_worldeffect)

    def on_move_unit(self, from_pos:"tuple[int,int]", to_pos:"tuple[int,int]"):
        """Move the UI version of the moved unit from the normal grid."""
        print("GridUI: Moving unit from", from_pos, "to", to_pos)
        uiunit = self.ui_units[self.grid.c_to_i(from_pos)]
        fsp = add(self.transform_grid_screen(from_pos), self.unit_draw_offset)
        tsp = add(self.transform_grid_screen(to_pos), self.unit_draw_offset)
        uiunit.set_interp_movement(fsp, tsp, .5)
        self.ui_units[self.grid.c_to_i(from_pos)] = None
        self.ui_units[self.grid.c_to_i(to_pos)] = uiunit
    
    def on_remove_unit(self, pos:"tuple[int,int]"):
        """Remove a UI-unit at the given position."""
        self.ui_units[self.grid.c_to_i(pos)] = None

    def on_remove_tile_effect(self, effect:"EffectBase", pos:"tuple[int,int]"):
        """Remove a UI-effect at the given position."""
        for uieffect in self.ui_worldeffects[self.grid.c_to_i(pos)][:]:
            if uieffect._parentelement == effect:
                self.ui_worldeffects[self.grid.c_to_i(pos)].remove(uieffect)
                return
       
    def on_remove_unit_effect(self, effect:"EffectBase", pos:"tuple[int,int]"):
        pass
        # """Remove a UI-effect at the given position."""
        # for uieffect in self.uiuniteffects[self.grid.c_to_i(pos)][:]:
        #     if uieffect._parentelement == effect:
        #         self.uieffects[self.grid.c_to_i(pos)].remove(uieffect)
        #         return

    def update(self, delta_time:float):
        """Update the graphics and animations' frames."""
        [x.update(delta_time) for x in self.ui_tiles if x]
        [x.update(delta_time) for x in self.ui_units if x]
        [x.update(delta_time) for y in self.ui_worldeffects for x in y if x]
    
    def on_load_map(self, map:Map):
        """Clear all the residual graphic objects, as they will be added during map load."""
        
    def get_unitui(self, pos:"tuple[int,int]"):
        """Return the UI-unit at given position."""
        return self.ui_units[self.grid.c_to_i(pos)]
   
    def get_tileui(self, pos:"tuple[int,int]"):
        """Return the UI-tile at given position."""
        return self.ui_tiles[self.grid.c_to_i(pos)]
    
    def get_tile_effectsui(self, pos:"tuple[int,int]"):
        """Return the UI-effects at given position."""
        return self.ui_worldeffects[self.grid.c_to_i(pos)]
    
    def get_unit_effectsui(self, pos:"tuple[int,int]"):
        """Return the UI-effects at given position."""
        return self.ui_unit_effects[self.grid.c_to_i(pos)]

    def transform_grid_world(self, gridpos:"tuple[int,int]"):
        """Return the world position of a given grid coordinate."""
        return (
            int( (gridpos[1]-gridpos[0]) * (self.tile_size[0]/2)),
            int( (gridpos[1]+gridpos[0]) * 22)
        )

    def transform_grid_screen(self, gridpos:"tuple[int,int]"):
        """Return the screen position of a given grid coordinate (i.e. applies camera pan)."""
        gw = self.transform_grid_world(gridpos)
        return add((int(gw[0] + (self.width-self.tile_size[0])/2), gw[1]+5), self.pan)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        grid_element:"GridElementUI|None"
        yield from self.blits
        self.blits.clear()
        for grid_element in self.ui_tiles:
            if grid_element:
                yield from grid_element.get_blits()
        for position in self.ui_worldeffects:
            for grid_element in position:
                yield from grid_element.get_blits()
        for grid_element in self.ui_units:
            if grid_element:
                yield from grid_element.get_blits()
    
    def _add_get_clear_blit(self):
        s = pygame.Surface(self.board_size)
        s.fill((0))
        self.blits.append((s, s.get_rect().move(self.pan),s.get_rect()))
