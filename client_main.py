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
from itblib.Log import log

import pygame
import pygame.display
import pygame.time
import os
import sys
import pygame.sprite
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

PIXELSIZE = 2
class Client:
    """The Client manages everything needed for a player on his machine, including graphics, the screen, etc."""
    def __init__(self) -> None:
        self.fps_cap = 30
        self.running = True
        self.playerfilepath = sys.argv[1]

        pygame.display.init()
        i = pygame.display.Info()
        self.screen_size = (i.current_w, i.current_h)
        self.scene_size = (int(self.screen_size[0]/PIXELSIZE), int(self.screen_size[1]/PIXELSIZE))
        self.screen = pygame.display.set_mode(self.screen_size, pygame.NOFRAME)
        self.scene_image = pygame.Surface(self.scene_size).convert_alpha()
        Textures.load_textures()
        pygame.font.init()
        
        self.scenemanager = SceneManager(scene_size=self.scene_size)
        
        self.connector = Connector(False)
        self.session = Session(NetEvents.connector)
      
        NetEvents.connector = self.connector
        NetEvents.session = self.session
        
        lobbyscene = LobbyScene(self.scenemanager, self.session)
        mainmenuscene = MainMenuScene(self.scenemanager)
        gamescene = GameScene(self.scenemanager, self.session)
        gamescene.gridui.update_pan( ((self.scene_image.get_width()-gamescene.gridui.board_size[0])/2, 0) )
        rosterselectionscene = RosterSelectionScene(self.scenemanager, self.playerfilepath)
        #mapselectionscene = MapSelectionScene(self.scenemanager)

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
        #self.scenemanager.add_scene("MapSelectionScene", mapselectionscene)
        #self.scenemanager.load_scene("LobbyScene")
        #self.scenemanager.load_scene("MainMenuScene")
        self.scenemanager.load_scene("RosterSelectionScene")

    def update_fullscreen(self, fullscreen:bool = False):
        return 

def main():
    log("Starting client...", 0)
    client = Client()
    log("Started client.", 0)
    while client.running:
        pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.running = False
            elif pygame.key.get_focused() and event.type == pygame.KEYDOWN:
                client.scenemanager._activescene.handle_key_event(event)
        dt = client.clock.tick(client.fps_cap)/1000.0
        client.scenemanager.update(dt)
        blits = []
        for blit in client.scenemanager._activescene.get_blits():
            s, r1, r2 = blit
            blits.append((s,r1,r2))
        client.scene_image.blits(blits)
        pygame.transform.scale(client.scene_image, client.screen.get_size(), client.screen)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
