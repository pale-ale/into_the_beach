from typing import TYPE_CHECKING

import pygame
import pygame.draw
import pygame.font
import pygame.transform

from pygame.surface import Surface

from itblib.globals.Colors import GREEN, RED
from itblib.globals.Enums import UNIT_IDS
from itblib.Player import PlayerData
from itblib.scenes.SceneBase import SceneBase
from itblib.ui.TextureManager import Textures
from itblib.ui.widgets.ui_widget import GridSelection, KeyIcon, TextBox, Widget
from itblib.ui.widgets.layout import HorizontalLayoutWidget

if TYPE_CHECKING:
    from typing import Generator

    from itblib.SceneManager import SceneManager


class RosterSelectionScene(SceneBase):
    """The user can select his lineup here."""
    def __init__(self, scenemanager:"SceneManager", playerfilepath:"str") -> None:
        super().__init__(scenemanager)
        self._VALID_UNITIDS = [1, 2, 3, 5, 6, 7, 8]
        self._TEXTCOLOR = (50,200,150,255)
        self._TEXTCOLOR_GRAY = (100,120,120,255)
        self._ELEMDIM = (64, 64)
        self._UNIT_SELECTION_COUNT = 3
        self._MAX_UNIT_COPIES = 3
        self._PLAYERFILEPATH = playerfilepath
        self._UNITLIST = GridSelection()
        self._TITLE_LAYOUT = HorizontalLayoutWidget(size=(self.scenemanager.scene_size[0],25))
        self._TITLE_LAYOUT.children = [TextBox(text="Select your lineup here.", textcolor=self._TEXTCOLOR, fontsize=32, oneline=True)]
        self._DESC_LAYOUT = HorizontalLayoutWidget(size=(self.scenemanager.scene_size[0],25))
        self._DESC_LAYOUT.position = (0, 25)

        self._KEYICON_ESC =     KeyIcon("ESC",    size=(23,23), fontsize=10)
        self._KEYICON_RETURN =  KeyIcon("\u23CE", size=(23,23), fontsize=16)
        self._KEYICON_SPACE =   KeyIcon("\u2423", size=(23,23), fontsize=16)
        
        self._TEXTBOX_ESC =     TextBox("Quit",             textcolor=self._TEXTCOLOR,      lineheight=15, oneline=True)
        self._TEXTBOX_RETURN =  TextBox("Select a Unit",    textcolor=self._TEXTCOLOR,      lineheight=15, oneline=True)
        self._TEXTBOX_SPACE =   TextBox("Save (Select 3)",  textcolor=self._TEXTCOLOR_GRAY, lineheight=15, oneline=True)

        self._DESC_ELEMENTS:list[Widget] = [
            self._KEYICON_ESC,      self._TEXTBOX_ESC,
            self._KEYICON_RETURN,   self._TEXTBOX_RETURN,
            self._KEYICON_SPACE,    self._TEXTBOX_SPACE
        ]
        self._DESC_LAYOUT.children = self._DESC_ELEMENTS

        self.image = pygame.Surface(self.scenemanager.scene_size)
        self.image.fill(0)
        self._unit_images:list[pygame.Surface] = []
        self._save_enabled = False

        self._UNITLIST.set_properties(
            size=self.scenemanager.scene_size,
            cursor_colour=(GREEN) if self._is_selection_valid(self._UNITLIST._selections) else RED)
        self._UNITLIST.position = (0, 50)
        self._UNITLIST.selection_update_callback = self._on_update_unit_selection

        self.register_input_listeners(self._UNITLIST)

    def load(self):
        super().load()
        self._setup_unit_images()
        self._UNITLIST.set_data_source(lambda i: self._unit_images[i], len(self._VALID_UNITIDS))

    #pylint: disable=missing-function-docstring
    def handle_key_event(self, event: any) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
                return True
            elif event.key == pygame.K_SPACE:
                selection = self._UNITLIST._selections
                if self._is_selection_valid(selection):
                    self._units_selected(selection)
                return True
        return super().handle_key_event(event)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.image, self.image.get_rect(), self.image.get_rect())
        yield from self._TITLE_LAYOUT.get_blits()
        yield from self._DESC_LAYOUT.get_blits()
        yield from self._UNITLIST.get_blits()

    def _is_selection_valid(self, selection:dict[int, int]) -> bool:
        if sum(selection.values()) != self._UNIT_SELECTION_COUNT:
            return False
        for unitidindex in selection.keys():
            if unitidindex < 0 or unitidindex >= len(self._VALID_UNITIDS):
                return False
        return True

    def _on_update_unit_selection(self, unit_selection:dict[int,int]):
        selection_valid = self._is_selection_valid(unit_selection)
        cursor_colour = GREEN if selection_valid else RED
        self._UNITLIST.set_properties(cursor_colour=cursor_colour)
        self._set_save_enabled(selection_valid)

    def _units_selected(self, unit_selection:dict[int,int]):
        if not self._save_enabled:
            return
        initialunits:dict[int,int] = {}
        for unitidindex, copycount in unit_selection.items():
            initialunits[self._VALID_UNITIDS[unitidindex]] = copycount
        PlayerData.load(self._PLAYERFILEPATH)
        PlayerData.roster = initialunits
        PlayerData.save(self._PLAYERFILEPATH)
        self._set_save_enabled(False)

    def _set_save_enabled(self, enabled:bool):
        self._save_enabled = enabled
        save_colour = self._TEXTCOLOR if enabled else self._TEXTCOLOR_GRAY
        self._TEXTBOX_SPACE.textcolor = save_colour
        self._TEXTBOX_SPACE.update_textbox()

    def _setup_unit_images(self):
        for unitid in self._VALID_UNITIDS:
            tex = Surface(self._ELEMDIM).convert_alpha()
            tex.fill((0))
            spritesheet = Textures.get_spritesheet(UNIT_IDS[unitid]+"SWIdle")
            if spritesheet:
                tex.blit(spritesheet[0], (0,0,64,64))
            else:
                raise Exception(f"RosterSelectionScene: Unitid \"{unitid}\" does not have an associated spritesheet.")
            self._unit_images.append(tex)
