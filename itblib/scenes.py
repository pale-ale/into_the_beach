"""
Scenes are a way to organize several Display-Objects as well as their functioniality,
essentially allowing for easy grouping and switching between them.

Scenes are managed by the SceneManager,
which is able to e.g. load() and unload() scenes before and after use, respectively.
"""
import random
from typing import TYPE_CHECKING

import pygame
import pygame.draw
import pygame.font
import pygame.image
import pygame.sprite
import pygame.surface
import pygame.transform

from itblib.globals.Colors import BLACK, GREEN, RED
from itblib.globals.Constants import DIRECTIONS
from itblib.globals.Enums import UNIT_IDS
from itblib.Grid import Grid
from itblib.input.Input import InputAcceptor
from itblib.Log import log
from itblib.Maps import Map, MapGrasslands, MapIceAge, MapRockValley
from itblib.net.NetEvents import NetEvents
from itblib.Player import PlayerData
from itblib.Selector import Selector
from itblib.ui.GridUI import GridUI
from itblib.ui.hud.hud import Hud
from itblib.ui.IGraphics import IGraphics
from itblib.ui.TextureManager import Textures
from itblib.ui.widgets.layout import HorizontalLayoutWidget
from itblib.ui.widgets.ui_widget import GridSelection, KeyIcon, TextBox, Widget
from itblib.Vec import smult
from itblib.audio import AudioManager, AUDIO_KEYS

if TYPE_CHECKING:
    from typing import Generator

    from itblib.Game import Session


class SceneManager:
    """Manages the Scenes."""
    def __init__(self, scene_size:"tuple[int,int]") -> None:
        self.scenes:"dict[str, SceneBase]" = {}
        self._activescene:"SceneBase" = None
        self.scene_size:"tuple[int,int]" = scene_size

    def load_scene(self, key:str):
        """Load a scene with the specified key."""
        if key in self.scenes:
            if self._activescene:
                self._activescene.unload()
            scene = self.scenes[key]
            self._activescene = scene
            log(f"SceneManager: Loading scene '{type(scene).__name__}'", 0)
            self._activescene.load()
        else:
            log(f"SceneManager: Unknown scene '{key}'", 2)

    def add_scene(self, key:str, scene:"SceneBase"):
        self.scenes[key] = scene

    def update(self, delta_time:float):
        if self._activescene:
            self._activescene.update(delta_time)


class SceneBase(IGraphics, InputAcceptor):
    """Base class for the other scenes"""

    def __init__(self, scenemanager:"SceneManager") -> None:
        IGraphics.__init__(self)
        InputAcceptor.__init__(self)
        self.scenemanager = scenemanager
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []

    def on_displayresize(self, newsize:"tuple[int,int]"):
        pass

    def update(self, delta_time:float):
        """Tick the scene."""
        if NetEvents.connector and NetEvents.connector.acc_connection:
            data = NetEvents.connector.receive_client()
            if data:
                prefix, contents = data
                NetEvents.rcv_event_caller(prefix, contents)

    def clear(self):
        """Fill the scene with solid black."""
        surf = pygame.Surface(self.scenemanager.scene_size)
        surf.fill(BLACK)
        self.blits.append((surf, surf.get_rect(), surf.get_rect()))

    def load(self):
        """Initialize a scene, load textures, etc."""
        self.clear()

    def unload(self):
        """Perform cleanup tasks."""


class MainMenuScene(SceneBase):
    """Main menu placeholder."""
    def __init__(self, scenemanager:"SceneManager") -> None:
        super().__init__(scenemanager)
        self.background = pygame.image.load("sprites/Splashscreen.png").convert_alpha()
        self.spottime = 0
        self.spotchangetime = .1
        self.lightspots:"list[tuple[int,int]]" = []

        width, height = self.background.get_size()
        tb_fullscreen = TextBox(text="Toggle Fullscreen", textcolor=(50,255,255,255), linewidth=100, fontsize=16, bgcolor=(255,100,255,150), pos=(350, 12))
        tb_map        = TextBox(text="Map Selection"    , textcolor=(50,255,255,255), linewidth=100, fontsize=16, bgcolor=(255,100,255,150), pos=(375, 37))
        tb_roster     = TextBox(text="Edit Roster"      , textcolor=(50,255,255,255), linewidth=100, fontsize=16, bgcolor=(255,100,255,150), pos=(400, 62))
        tb_battle     = TextBox(text="Battle"           , textcolor=(50,255,255,255), linewidth= 40, fontsize=16, bgcolor=(255,100,255,150), pos=(width/2 - 26-15, height*.805))
        tb_settings   = TextBox(text="Game Settings"    , textcolor=(50,255,255,255), linewidth= 75, fontsize=16, bgcolor=(255,100,255,150), pos=(width/2 + 26+29, height*.87 ))
        tb_loadout    = TextBox(text="Loadout"          , textcolor=(50,255,255,255), linewidth= 50, fontsize=16, bgcolor=(255,100,255,150), pos=(width/2 - 26-52, height*.87 ))
        tb_exit       = TextBox(text="Exit"             , textcolor=(50,255,255,255), linewidth= 40, fontsize=16, bgcolor=(255,100,255,150), pos=(width/2 + 25   , height*.945))

        self.textsprites = [
            tb_fullscreen, tb_roster, tb_map,
            tb_battle, tb_settings, tb_loadout, tb_exit
        ]

        ki_up    = KeyIcon('↑', size=(26,26), pos=(width/2   , height*.8))
        ki_left  = KeyIcon('←', size=(26,26), pos=(width/2-30, height*.85), enabled=False, pressed=True)
        ki_right = KeyIcon('→', size=(26,26), pos=(width/2+30, height*.85), enabled=False, pressed=True)
        ki_down  = KeyIcon('↓', size=(26,26), pos=(width/2   , height*.9 ), enabled=False, pressed=True)
        ki_f     = KeyIcon('F', size=(26,26), pos=(325,   5))
        ki_m     = KeyIcon('M', size=(26,26), pos=(350,  30))
        ki_r     = KeyIcon('R', size=(26,26), pos=(375,  55))

        self.keysprites = [
            ki_up, ki_left, ki_right, ki_down,
            ki_f, ki_r, ki_m
        ]

    def load(self):
        super().load()
        self.blits.append((self.background, self.background.get_rect(), self.background.get_rect()))
        self.lightspots:"list[tuple[int,int]]" = self._get_lightspots()
        for i in range(len(self.lightspots)):
            self._set_light(i)

    #pylint: disable=missing-function-docstring
    def handle_key_event(self, event: any) -> bool:
        if super().handle_key_event(event):
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit(0)
            if event.key == pygame.K_UP:
                AudioManager.play_audio(AUDIO_KEYS.BUTTON)
                self.scenemanager.load_scene("LobbyScene")
                return True
            if event.key == pygame.K_r:
                AudioManager.play_audio(AUDIO_KEYS.BUTTON)
                self.scenemanager.load_scene("RosterSelectionScene")
                return True
            if event.key == pygame.K_m:
                AudioManager.play_audio(AUDIO_KEYS.BUTTON)
                self.scenemanager.load_scene("MapSelectionScene")
                return True
        return False

    def _get_lightspots(self):
        lightspots:"list[tuple[int,int]]" = []
        lightspots.extend([(x,y) for x in range( 45,  62, 3) for y in range (65, 112, 4)])
        lightspots.extend([(x,y) for x in range( 79,  89, 3) for y in range (85, 112, 4)])
        lightspots.extend([(x,y) for x in range(122, 135, 3) for y in range (42, 112, 4)])
        lightspots.extend([(x,y) for x in range(157, 175, 3) for y in range (42, 112, 4)])
        return lightspots

    def _set_light(self, index:int, color:"tuple[int,int,int,int]|None"=None):
        pos = self.lightspots[index]
        if color:
            self.background.set_at(pos, color)
        else:
            self.background.set_at(pos, (200,200,255,255) if random.randint(0,1) else (0,0,0,255))
        self.blits.append((self.background, pygame.Rect(*pos,1,1), pygame.Rect(*pos,1,1)))

    def update(self, delta_time: float):
        self.spottime += delta_time
        if self.spottime > self.spotchangetime:
            self.spottime = 0
            index = random.randrange(0, len(self.lightspots))
            self._set_light(index)
        return super().update(delta_time)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits
        child:Widget
        for child in self.keysprites + self.textsprites:
            yield from child.get_blits()
        self.blits.clear()


class LobbyScene(SceneBase):
    """
    The LobbyScene displays some general match info,
    like it's participants and their user names, levels,
    the map, the game mode etc..
    """
    def __init__(self, scenemanager: "SceneManager", session:"Session") -> None:
        super().__init__(scenemanager)
        self._session = session
        self.font = pygame.font.Font("HighOne.ttf", 16)
        self.loaded_gamescene = False
        self.image = pygame.Surface(scenemanager.scene_size)
        self.image.fill(BLACK)
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []

    def load(self):
        super().load()
        self.loaded_gamescene = False
        if NetEvents.connector:
            NetEvents.connector.client_connect()

    def update_data(self):
        """Display the updated list of the players."""
        if self._session._state in ["running", "runningPregame"]:
            if not self.loaded_gamescene:
                self.loaded_gamescene = True
                self.scenemanager.load_scene("GameScene")
                return
        elif self.loaded_gamescene:
            self.scenemanager.load_scene("MainMenuScene")
            return
        self.image.fill(BLACK)
        y = 0
        header = self.font.render(f"Waiting for players ({len(self._session._players)}/2)...", False, (100,255,255,255))
        self.image.blit(header, (self.image.get_width()/2-header.get_width()/2, 50))
        for player in self._session._players.values():
            nametag = self.font.render(
                f"{player.name.ljust(45)}LVL: {str(player.level).zfill(3)}",
                False, player.color, (100,100,100,255)
            )
            self.image.blit(nametag, (100, 100+y))
            y += 100
        self.blits.append((self.image, self.image.get_rect(), self.image.get_rect()))

    def handle_key_event(self, keyevent):
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                NetEvents.snd_netplayerleave([p for p in self._session._players.values() if p.localcontrol][0].playerid)
                self.scenemanager.load_scene("MainMenuScene")

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits


class GameScene(SceneBase):
    """Contains the main game (grid, hud, etc.)"""
    def __init__(self, scenemanager:"SceneManager", session:"Session") -> None:
        super().__init__(scenemanager)
        self.grid = Grid(NetEvents.connector)
        self.gridui = GridUI(self.grid)
        self.grid.update_observer(self.gridui) 
        self.hud = Hud(scenemanager.scene_size, self.gridui, 0, session)
        self.selector = Selector(self.grid, self.hud)
        self.register_input_listeners(self.selector, self.hud)

    def load(self):
        super().load()
        self.hud.on_start_game()

    #pylint: disable=missing-function-docstring
    def handle_key_event(self, event) -> bool:
        if super().handle_key_event(event):
            return True
        if event.type == pygame.KEYDOWN:
            pan = self.gridui._pan
            if event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_UP:
                self.gridui.update_pan((pan[0], pan[1] + 2*22*self.hud.displayscale))
                self.selector.move_cursor(DIRECTIONS.NORTH)
                self.selector.move_cursor(DIRECTIONS.NORTH)
                self.hud.update_cursor()
                return True
            if event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_DOWN:
                self.gridui.update_pan((pan[0], pan[1] - 2*22*self.hud.displayscale))
                self.selector.move_cursor(DIRECTIONS.SOUTH)
                self.selector.move_cursor(DIRECTIONS.SOUTH)
                self.hud.update_cursor()
                return True
            if event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_LEFT:
                self.gridui.update_pan((pan[0]+2*32*self.hud.displayscale, pan[1]))
                self.selector.move_cursor(DIRECTIONS.WEST)
                self.selector.move_cursor(DIRECTIONS.WEST)
                self.hud.update_cursor()
                return True
            if event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_RIGHT:
                self.gridui.update_pan((pan[0]-2*32*self.hud.displayscale, pan[1]))
                self.selector.move_cursor(DIRECTIONS.EAST)
                self.selector.move_cursor(DIRECTIONS.EAST)
                self.hud.update_cursor()
                return True
            if event.key == pygame.K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
                return True
        return False

    def update(self, delta_time:float):
        super().update(delta_time)
        self.grid.tick(delta_time)
        self.gridui.update(delta_time)
        self.hud.update(delta_time)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits
        self.blits.clear()
        yield from self.gridui.get_blits()
        yield from self.hud.get_blits()


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
            if event.key == pygame.K_SPACE:
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
            tex = pygame.Surface(self._ELEMDIM).convert_alpha()
            tex.fill((0))
            spritesheet = Textures.get_spritesheet(UNIT_IDS[unitid]+"SWIdle")
            if spritesheet:
                tex.blit(spritesheet[0], (0,0,64,64))
            else:
                raise Exception(f"RosterSelectionScene:\
                    Unitid \"{unitid}\" does not have an associated spritesheet."
                )
            self._unit_images.append(tex)


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

        self._MAPLIST.set_properties(
            size=self.scenemanager.scene_size,
            cursor_colour=(GREEN) if self._is_selection_valid(self._MAPLIST._selections) else RED,
            elem_size=self._ELEMDIM,
            paddings=(3,1))
        self._MAPLIST.position = (0, 50)
        self._MAPLIST.selection_update_callback = self._on_update_unit_selection

        self.register_input_listeners(self._MAPLIST)

    def load(self):
        super().load()
        self._setup_map_images()
        self._MAPLIST.set_data_source(lambda i: self._map_images[i], len(self._VALID_MAPS))

    #pylint: disable=missing-function-docstring
    def handle_key_event(self, event: any) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
                return True
            if event.key == pygame.K_SPACE:
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
        self._MAPLIST.set_properties(cursor_colour=cursor_colour)
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

    def _setup_map_images(self):
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
