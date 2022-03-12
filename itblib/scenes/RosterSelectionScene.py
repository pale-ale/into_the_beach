from typing import Generator

import itblib
import pygame
import pygame.draw
import pygame.font
import pygame.transform
from itblib.globals.Colors import GREEN, RED
from itblib.globals.Enums import UNIT_IDS
from itblib.Player import PlayerData
from itblib.SceneManager import SceneManager
from itblib.scenes.SceneBase import SceneBase
from itblib.ui.TextureManager import Textures
from itblib.ui.widgets.GridSelection import GridSelection
from itblib.ui.widgets.TextBox import TextBox
from itblib.Vec import add, get_translation_for_center
from pygame.surface import Surface


class RosterSelectionScene(SceneBase):
    """The user can select his lineup here."""
    def __init__(self, scenemanager:"SceneManager", playerfilepath:"str") -> None:
        super().__init__(scenemanager)
        self._UNITIDS = [1, 2, 3, 5, 6, 7, 8]
        self._ELEMDIM = (64, 64)
        self._UNIT_SELECTION_COUNT = 3
        self._MAX_UNIT_COPIES = 3
        self._PLAYERFILEPATH = playerfilepath
        self._UNITLIST = GridSelection()
        self._TITLE_TEXTBOX = TextBox(text="Select your lineup here.", textcolor=(50,200,150,255), fontsize=32, linewidth=280)
        self._DESC_TEXTBOX = TextBox(text="[ESC] to quit, [SPACE] to save when 3 units have been selected, \
             [ENTER] to add/remove unit", textcolor=(50,200,150,255), linewidth=480, lineheight=15)

        self.image = pygame.Surface(self.scenemanager.scene_size)
        self._unit_images:list[pygame.Surface] = []
        
        self._TITLE_TEXTBOX.position = get_translation_for_center(
            self._TITLE_TEXTBOX.position, self._TITLE_TEXTBOX.get_size(),
            (0,0), self.scenemanager.scene_size, vertical=False)
        self._DESC_TEXTBOX.position = add((0,25), get_translation_for_center(
            self._DESC_TEXTBOX.position, self._DESC_TEXTBOX.get_size(),
            self._TITLE_TEXTBOX.position, self._TITLE_TEXTBOX.get_size(),
            vertical=False))
        self._UNITLIST.setProperties(
            size=self.scenemanager.scene_size,
            cursor_colour=(GREEN) if sum(self._UNITLIST._selections) == self._UNIT_SELECTION_COUNT else RED)
        self._UNITLIST.position = (0, 50)
        self._UNITLIST.selection_update_callback = self._on_update_unit_selection
        
        self.register_input_listeners(self._UNITLIST)
    
    def load(self):
        super().load()
        self._setup_unit_images()
        self._UNITLIST.set_data_source(lambda i: self._unit_images[i] , len(self._UNITIDS))

    def handle_key_event(self, event: any) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
                return True
        return super().handle_key_event(event)

    def _on_update_unit_selection(self, unit_selection:list[int]):
        enough_selected = sum(unit_selection) == self._UNIT_SELECTION_COUNT
        self._UNITLIST.setProperties(cursor_colour=(GREEN) if enough_selected else RED)
        if enough_selected:
            self._units_selected(unit_selection)

    def _units_selected(self, unit_selection:list[int]):
        initialunits = []
        for index in range(len(unit_selection)):
            for i in range(unit_selection[index]):
                initialunits.append(self._UNITIDS[index])
        PlayerData.load(self._PLAYERFILEPATH)
        PlayerData.roster = initialunits
        PlayerData.save(self._PLAYERFILEPATH)
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self._TITLE_TEXTBOX.get_blits()
        yield from self._DESC_TEXTBOX.get_blits()
        yield from self._UNITLIST.get_blits()

    def _setup_unit_images(self):
        for unitid in self._UNITIDS:
            tex = Surface(self._ELEMDIM).convert_alpha()
            tex.fill((0))
            spritesheet = Textures.get_spritesheet(UNIT_IDS[unitid]+"SWIdle")
            if spritesheet:
                tex.blit(spritesheet[0], (0,0,64,64))
            else:
                raise Exception(f"RosterSelectionScene: Unitid \"{unitid}\" does not have an associated spritesheet.")
            self._unit_images.append(tex)
