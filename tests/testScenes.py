import unittest

import pygame
from itblib.Game import Session
from itblib.Player import Player
from itblib.scenes import (GameScene, LobbyScene, MainMenuScene,
                           MapSelectionScene, RosterSelectionScene,
                           SceneManager)
from itblib.ui.TextureManager import Textures


class TestScenes(unittest.TestCase):
    def setUp(self) -> None:
        screensize = (300,300)
        self.scenemanager = SceneManager(screensize)
        pygame.display.set_mode(screensize)
        pygame.font.init()
        pygame.display.init()

    def test_main_menu_scene(self):
        mmscene = MainMenuScene(self.scenemanager)
        self.scenemanager.add_scene("mainmenutest", mmscene)
        self.scenemanager.load_scene("mainmenutest")
    
    def test_lobby_scene(self):
        session = Session(None)
        lobbyscene = LobbyScene(self.scenemanager, session)
        self.scenemanager.add_scene("LobbyScene", lobbyscene)
        self.scenemanager.load_scene("LobbyScene")

    def test_roster_selection_scene(self):
        Textures.load_textures()
        rosterselectionscene = RosterSelectionScene(self.scenemanager, "playerdata1.json")
        self.scenemanager.add_scene("RosterSelectionScene", rosterselectionscene)
        self.scenemanager.load_scene("RosterSelectionScene")

    def test_game_scene(self):
        session = Session(None)
        session.add_player(Player(0, None))
        session.add_player(Player(1, None))
        gamescene = GameScene(self.scenemanager, session)
        self.scenemanager.add_scene("GameScene", gamescene)
        self.scenemanager.load_scene("GameScene")

    def test_map_selection_scene(self):
        Textures.load_textures()
        mapselectionscene = MapSelectionScene(self.scenemanager, "playerdata1.json")
        self.scenemanager.add_scene("MapSelectionScene", mapselectionscene)
        self.scenemanager.load_scene("MapSelectionScene")
