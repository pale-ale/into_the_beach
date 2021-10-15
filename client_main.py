from itblib.net.Connector import Connector
from itblib.Game import Session
from itblib.scenes.GameScene import GameScene
from itblib.scenes.MainMenuScene import MainMenuScene
from itblib.scenes.MapSelectionScene import MapSelectionScene
from itblib.scenes.LobbyScene import LobbyScene
from itblib.net.NetEvents import NetEvents
from itblib.Player import PlayerData
from itblib.scenes.RosterSelectionScene import RosterSelectionScene
from itblib.SceneManager import SceneManager
from itblib.Selector import Selector
from itblib.ui.TextureManager import Textures

import pygame
import pygame.display
import pygame.time
import os
import sys
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

class Client:
    """The Client manages everything needed for a player on his machine, including graphics, the screen, etc."""
    def __init__(self) -> None:
        self.fps_cap = 30
        self.normal_displaysize = (1280, 640)
        self.displaysize = self.normal_displaysize
        self.running = True
        self.playerfilepath = sys.argv[1]

        pygame.display.init()
        self.screen = pygame.display.set_mode(self.displaysize, pygame.NOFRAME)
        Textures.load_textures()
        pygame.font.init()
        
        self.scenemanager = SceneManager()
        
        self.connector = Connector(False)
        self.session = Session(NetEvents.connector)
      
        NetEvents.connector = self.connector
        NetEvents.session = self.session
        
        lobbyscene = LobbyScene(self.scenemanager, *self.displaysize, self.session)
        mainmenuscene = MainMenuScene(self, self.scenemanager, *self.displaysize)
        gamescene = GameScene(self.scenemanager, *self.displaysize)
        rosterselectionscene = RosterSelectionScene(self.scenemanager, *self.displaysize)
        mapselectionscene = MapSelectionScene(self.scenemanager, *self.displaysize)

        self.session._observer = lobbyscene

        PlayerData.load(self.playerfilepath)
        self.fullscreen_displaysize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        pygame.display.set_caption("Into The Bleach (for covid purposes only)")
        self.displayinfo = pygame.display.Info()
        self.clock = pygame.time.Clock()
        NetEvents.grid = gamescene.grid
        NetEvents.hud = gamescene.hud
        NetEvents.scenemanager = self.scenemanager
        self.selector = Selector(gamescene.grid, gamescene.hud)
        self.scenemanager.add_scene("GameScene", gamescene)
        self.scenemanager.add_scene("LobbyScene", lobbyscene)
        self.scenemanager.add_scene("MainMenuScene", mainmenuscene)
        self.scenemanager.add_scene("RosterSelectionScene", rosterselectionscene)
        self.scenemanager.add_scene("MapSelectionScene", mapselectionscene)
        self.scenemanager.load_scene("MainMenuScene")

    def update_fullscreen(self, fullscreen:bool = False):
        if fullscreen:
            self.screen = pygame.display.set_mode(self.fullscreen_displaysize, pygame.NOFRAME)
            self.scenemanager.scenes["GameScene"].on_displayresize(self.fullscreen_displaysize)
        else:
            # this actually needs to be called 2 times for god knows why.
            self.scenemanager.scenes["GameScene"].on_displayresize(self.normal_displaysize)
            self.screen = pygame.display.set_mode(self.normal_displaysize, pygame.NOFRAME).convert_alpha()
            self.screen = pygame.display.set_mode(self.normal_displaysize, pygame.NOFRAME).convert_alpha()

def main():
    client = Client()

    while client.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.running = False
            elif pygame.key.get_focused() and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                client.scenemanager._activescene.on_keyevent(event)
        dt = client.clock.tick(client.fps_cap)/1000.0
        client.scenemanager.update(dt) 
        client.screen.fill((0,0,0,0))
        client.screen.blit(client.scenemanager._activescene.image, (0,0))
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
