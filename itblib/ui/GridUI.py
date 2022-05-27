import pygame
from itblib.components import ComponentAcceptor, TransformComponent
from itblib.globals.Constants import STANDARD_TILE_SIZE
from itblib.globals.factories import GridElementUIFactory
from itblib.Grid import Grid
from itblib.gridelements.world_effects import WorldEffectBase
from itblib.gridelements.ui_effect import EffectBaseUI
from itblib.gridelements.GridElementUI import GridElementUI
from itblib.gridelements.Tiles import TileBase
from itblib.gridelements.TilesUI import TileBaseUI
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.gridelements.UnitsUI import UnitBaseUI
from itblib.ui.IGridObserver import IGridObserver
from itblib.ui.IGraphics import IGraphics
from itblib.Vec import IVector2


class GridUI(IGraphics, ComponentAcceptor, IGridObserver):
    """The Graphical representation of the grid."""
    def __init__(self, grid: Grid):
        IGraphics.__init__(self)
        ComponentAcceptor.__init__(self)
        self.tfc = TransformComponent()
        self.tfc.attach_component(self)
        self.grid = grid
        self.tile_size = IVector2(*STANDARD_TILE_SIZE)
        left_tile = self.transform_grid_world(IVector2(grid.size.x-1, 0))
        right_tile = self.transform_grid_world(IVector2(0, grid.size.y-1))
        bottom_tile = self.transform_grid_world(IVector2(grid.size.x-1, grid.size.y-1))
        self.width = right_tile.x - left_tile.x + self.tile_size.x
        self.height = bottom_tile.y + self.tile_size.y
        self.board_size = (self.width, self.height)
        self.ui_tiles: "list[TileBaseUI|None]" = [None]*grid.size.x*grid.size.y
        self.ui_worldeffects: "list[list[EffectBaseUI]]" = [[] for i in range(grid.size.x*grid.size.y)]
        self.ui_units: "list[UnitBaseUI|None]" = [None]*grid.size.x*grid.size.y
        self.ui_unit_effects: "list[list[EffectBaseUI]]" = [[] for i in range(grid.size.x*grid.size.y)]
        self.unit_draw_offset = IVector2(0, -10)
        self._pan = IVector2(0, 0)
        self.phase_change_callback = None
        self.blits: "list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
        self._dbgsurf = None

    def on_change_phase(self, phase: int):
        if phase == 2:
            self._add_get_clear_blit()
        if self.phase_change_callback:
            self.phase_change_callback(phase)

    def on_add_tile(self, tile: TileBase):
        """Add the UI version of the new tile added to the normal grid."""
        ui_tile_class = GridElementUIFactory.find_tile_class(type(tile).__name__ + "UI")
        if ui_tile_class:
            ui_tile = ui_tile_class(tile)
            self.ui_tiles[self.grid.c_to_i(tile.pos)] = ui_tile
            self.add_gridui_element(ui_tile)

    def update_pan(self, newpan: IVector2):
        assert isinstance(newpan, IVector2)
        self._add_get_clear_blit()
        self._pan = newpan
        self.tfc.relative_position = newpan

    def add_gridui_element(self, elem: GridElementUI):
        elem_tfc = elem.get_component(TransformComponent)
        elem_tfc.relative_position = self.transform_grid_screen(elem._parentelement.pos, apply_pan=False)
        elem_tfc.set_transform_target(self)

    def on_add_unit(self, unit: UnitBase):
        """Add the UI version of the new unit added to the normal grid."""
        ui_unit_class = GridElementUIFactory.find_unit_class(type(unit).__name__ + "UI")
        if ui_unit_class:   
            ui_unit:UnitBaseUI = ui_unit_class(unit)
            self.ui_units[self.grid.c_to_i(unit.pos)] = ui_unit
            self.add_gridui_element(ui_unit)
            tfc = ui_unit.get_component(TransformComponent)
            tfc.relative_position = tfc.relative_position + self.unit_draw_offset
    
    def on_add_worldeffect(self, effect: WorldEffectBase):
        """Add the UI version of the new effect added to the normal grid."""
        gridindex = self.grid.c_to_i(effect.pos)
        ui_worldeffect_class = GridElementUIFactory.find_effect_class(type(effect).__name__ + "UI")
        if ui_worldeffect_class:
            ui_worldeffect = ui_worldeffect_class(effect)
            self.ui_worldeffects[gridindex].append(ui_worldeffect)
            self.add_gridui_element(ui_worldeffect)

    def on_move_unit(self, from_pos: IVector2, to_pos: IVector2):
        """Move the UI version of the moved unit from the normal grid."""
        assert isinstance(from_pos, IVector2)
        assert isinstance(to_pos, IVector2)
        uiunit = self.ui_units[self.grid.c_to_i(from_pos)]
        fsp = add(self.transform_grid_screen(from_pos, apply_pan=False), self.unit_draw_offset)
        tsp = add(self.transform_grid_screen(to_pos, apply_pan=False), self.unit_draw_offset)
        uiunit.set_interp_movement(fsp, tsp, .5)
        self.ui_units[self.grid.c_to_i(from_pos)] = None
        self.ui_units[self.grid.c_to_i(to_pos)] = uiunit
    
    def on_remove_unit(self, pos: "tuple[int,int]"):
        """Remove a UI-unit at the given position."""
        self.ui_units[self.grid.c_to_i(pos)] = None

    def on_remove_worldeffect(self, effect: "WorldEffectBase", pos: "tuple[int,int]"):
        """Remove a UI-effect at the given position."""
        for uieffect in self.ui_worldeffects[self.grid.c_to_i(pos)][:]:
            if uieffect._parentelement == effect:
                self.ui_worldeffects[self.grid.c_to_i(pos)].remove(uieffect)
                return

    def on_remove_tile(self, pos: "tuple[int,int]"):
        """Remove a UI-Tile at given position."""
        self.ui_tiles[self.grid.c_to_i(pos)] = None

    def on_remake_grid(self):
        pass

    def update(self, delta_time: float):
        """Update the graphics and animations' frames."""
        [x.tick(delta_time) for x in self.ui_tiles if x]
        [x.update(delta_time) for x in self.ui_units if x]
        [x.tick(delta_time) for y in self.ui_worldeffects for x in y if x]

    def get_unitui(self, pos: "tuple[int,int]"):
        """Return the UI-unit at given position."""
        return self.ui_units[self.grid.c_to_i(pos)]

    def get_tileui(self, pos: "tuple[int,int]"):
        """Return the UI-tile at given position."""
        return self.ui_tiles[self.grid.c_to_i(pos)]

    def get_tile_effectsui(self, pos: "tuple[int,int]"):
        """Return the UI-effects at given position."""
        return self.ui_worldeffects[self.grid.c_to_i(pos)]

    def get_unit_effectsui(self, pos: "tuple[int,int]"):
        """Return the UI-effects at given position."""
        return self.ui_unit_effects[self.grid.c_to_i(pos)]

    def transform_grid_world(self, gridpos: IVector2) -> IVector2:
        """Return the world position of a given grid coordinate."""
        x = (gridpos.y - gridpos.x) * (self.tile_size.x/2)
        y = (gridpos.y + gridpos.x) * 22
        return IVector2(int(x), int(y))

    def transform_grid_screen(self, gridpos: IVector2, apply_pan: bool = True):
        """Return the screen position of a given grid coordinate (can apply camera and center _pan)."""
        gw = self.transform_grid_world(gridpos)
        screennopan = IVector2(int(gw.x + (self.width-self.tile_size.x)/2), gw.y+5)
        return (screennopan + self._pan) if apply_pan else screennopan

    def get_blits(self):
        yield from self.blits
        self.blits.clear()
        grid_element: "GridElementUI|None"
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
        self.blits.append((s, s.get_rect().move(self._pan.c), s.get_rect()))

    def get_debug_surface(self):
        if self._dbgsurf:
            return self._dbgsurf
        self._dbgsurf = pygame.Surface(add(self.board_size, (2,2))).convert_alpha()
        self._dbgsurf.fill(0)
        offset = (32,8)
        for x in range(0, self.grid.size.x+1):
            pygame.draw.line(self._dbgsurf, (255,0,255), 
                add(self.transform_grid_screen((x,                0), apply_pan=False), offset),
                add(self.transform_grid_screen((x,self.grid.size.y), apply_pan=False), offset),
                1)
        for y in range(0, self.grid.size.y+1):
            pygame.draw.line(self._dbgsurf, (255,0,255), 
                add(self.transform_grid_screen((0,                y), apply_pan=False), offset), 
                add(self.transform_grid_screen((self.grid.size.x,y), apply_pan=False), offset),
                1)
        return self._dbgsurf
