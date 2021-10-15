from itblib.net.NetEvents import NetEvents
from itblib.scenes.SceneBase import SceneBase
from itblib.SceneManager import SceneManager
from itblib.Game import Session

import pygame.font

class LobbyScene(SceneBase):
    def __init__(self, scenemanager: "SceneManager", width: int, height: int, session:"Session") -> None:
        super().__init__(scenemanager, width, height)
        self._session = session
        self.font = pygame.font.SysFont("latinmodernmono", 20)
        self.loaded_gamescene = False
    
    def load(self):
        super().load()
        self.loaded_gamescene = False
        NetEvents.connector.client_init()

    def update_data(self):
        if self._session._state in ["running", "runningPregame"]:
            if not self.loaded_gamescene:
                self.loaded_gamescene = True
                self.scenemanager.load_scene("GameScene")
        elif self.loaded_gamescene:
            self.scenemanager.load_scene("MainMenuScene")
        self.image.fill(0)
        y = 0
        header = self.font.render(f"Waiting for players ({len(self._session._players)}/2)...", True, (100,255,255,255))
        self.image.blit(header, (self.image.get_width()/2-header.get_width()/2, 50))
        for player in self._session._players.values():
            nametag = self.font.render(player.name.ljust(45) + "LVL: "+str(player.level).zfill(3), True, player.color, (100,100,100,255))
            self.image.blit(nametag, (100, 100+y))
            y += 100

    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                NetEvents.snd_netplayerleave([p for p in self._session._players.values() if p.localcontrol][0])
                self.scenemanager.load_scene("MainMenuScene")
