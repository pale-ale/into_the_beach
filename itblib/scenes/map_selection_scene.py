from typing import TYPE_CHECKING

import pygame
import pygame.draw
import pygame.font
import pygame.transform
import pygame.surface

from itblib.globals.Colors import GREEN, RED
from itblib.Grid import Grid
from itblib.Maps import Map, MapGrasslands, MapIceAge, MapRockValley
from itblib.Player import PlayerData
from itblib.scenes.SceneBase import SceneBase
from itblib.ui.GridUI import GridUI
from itblib.ui.widgets.GridSelection import GridSelection
from itblib.ui.widgets.horizontal_layout import HorizontalLayoutWidget
from itblib.ui.widgets.KeyIcon import KeyIcon
from itblib.ui.widgets.TextBox import TextBox
from itblib.ui.widgets.Widget import Widget
from itblib.Vec import smult

if TYPE_CHECKING:
    from itblib.SceneManager import SceneManager
    from typing import Generator

class MapSelectionScene(SceneBase):
    """The user can select which maps to queue for here."""
    def __init__(self, scenemanager:"SceneManager", playerfilepath:"str") -> None:
        super().__init__(scenemanager)
        self._VALID_MAPS:list[Map] = [MapGrasslands(), MapIceAge(), MapRockValley()]
        self._TEXTCOLOR = (50,200,150,255)
        self._TEXTCOLOR_GRAY = (100,120,120,255)
        self._ELEMDIM = (164*1.3, 164)
        self._MAP_SELECTION_COUNT = int(len(self._VALID_MAPS)/2)+1
        self._PLAYERFILEPATH = playerfilepath
        self._MAPLIST = GridSelection()
        self._TITLE_LAYOUT = HorizontalLayoutWidget(size=(self.scenemanager.scene_size[0],25))
        self._TITLE_LAYOUT.children = [TextBox(text="Select the maps you want to queue for here.", textcolor=self._TEXTCOLOR, fontsize=32, oneline=True)]
        self._DESC_LAYOUT = HorizontalLayoutWidget(size=(self.scenemanager.scene_size[0],25))
        self._DESC_LAYOUT.position = (0, 25)
        self._KEYICON_ESC =     KeyIcon("ESC",    size=(23,23), fontsize=10)
        self._KEYICON_RETURN =  KeyIcon("\u23CE", size=(23,23), fontsize=16)
        self._KEYICON_SPACE =   KeyIcon("\u2423", size=(23,23), fontsize=16)
        
        self._TEXTBOX_ESC =     TextBox("Quit",             textcolor=self._TEXTCOLOR,      lineheight=15, oneline=True)
        self._TEXTBOX_RETURN =  TextBox("Select a map",     textcolor=self._TEXTCOLOR,      lineheight=15, oneline=True)
        self._TEXTBOX_SPACE =   TextBox(f"Save (Select at least {self._MAP_SELECTION_COUNT} maps)",  textcolor=self._TEXTCOLOR_GRAY, lineheight=15, oneline=True)

        self._DESC_ELEMENTS:list[Widget] = [
            self._KEYICON_ESC,      self._TEXTBOX_ESC,
            self._KEYICON_RETURN,   self._TEXTBOX_RETURN,
            self._KEYICON_SPACE,    self._TEXTBOX_SPACE
        ]
        self._DESC_LAYOUT.children = self._DESC_ELEMENTS

        self.image = pygame.Surface(self.scenemanager.scene_size)
        self.image.fill(0)
        self._map_images:"list[pygame.Surface]" = []
        self._save_enabled = False

        self._MAPLIST.setProperties(
            size=self.scenemanager.scene_size,
            cursor_colour=(GREEN) if self._is_selection_valid(self._MAPLIST._selections) else RED,
            elem_size=self._ELEMDIM, 
            paddings=(3,1))
        self._MAPLIST.position = (0, 50)
        self._MAPLIST.selection_update_callback = self._on_update_unit_selection

        self.register_input_listeners(self._MAPLIST)

    def load(self):
        super().load()
        self._setup_unit_images()
        self._MAPLIST.set_data_source(lambda i: self._map_images[i], len(self._VALID_MAPS))

    #pylint: disable=missing-function-docstring
    def handle_key_event(self, event: any) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
                return True
            elif event.key == pygame.K_SPACE:
                selection = self._MAPLIST._selections
                if self._is_selection_valid(selection):
                    self._maps_selected(selection)
                return True
        return super().handle_key_event(event)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.image, self.image.get_rect(), self.image.get_rect())
        yield from self._TITLE_LAYOUT.get_blits()
        yield from self._DESC_LAYOUT.get_blits()
        yield from self._MAPLIST.get_blits()

    def _is_selection_valid(self, selection:dict[int, int]) -> bool:
        if sum(selection.values()) < self._MAP_SELECTION_COUNT:
            return False
        for mapindex in selection.keys():
            if mapindex < 0 or mapindex >= len(self._VALID_MAPS):
                return False
        return True

    def _on_update_unit_selection(self, unit_selection:dict[int,int]):
        selection_valid = self._is_selection_valid(unit_selection)
        cursor_colour = GREEN if selection_valid else RED
        self._MAPLIST.setProperties(cursor_colour=cursor_colour)
        self._set_save_enabled(selection_valid)

    def _maps_selected(self, map_selection:dict[int,int]):
        if not self._save_enabled:
            return
        maps:list[Map] = []
        for mapindex in map_selection.keys():
            maps.append(type(self._VALID_MAPS[mapindex]).__name__)
        PlayerData.load(self._PLAYERFILEPATH)
        PlayerData.desired_maps = maps
        PlayerData.save(self._PLAYERFILEPATH)
        self._set_save_enabled(False)

    def _set_save_enabled(self, enabled:bool):
        self._save_enabled = enabled
        save_colour = self._TEXTCOLOR if enabled else self._TEXTCOLOR_GRAY
        self._TEXTBOX_SPACE.textcolor = save_colour
        self._TEXTBOX_SPACE.update_textbox()

    def _setup_unit_images(self):
        grid = Grid(None)
        gridui = GridUI(grid)
        grid.update_observer(gridui)
        for _map in self._VALID_MAPS:
            grid.load_map(_map)
            gridui.update(0.1)
            griduisize = (gridui.width, gridui.height)
            tex = pygame.Surface(griduisize).convert_alpha()
            tex.fill((0))
            tex.blits(gridui.get_blits())
            scale = min(self._ELEMDIM[0]/griduisize[0], self._ELEMDIM[1]/griduisize[1])
            self._map_images.append(pygame.transform.scale(tex, smult(scale, griduisize)))
