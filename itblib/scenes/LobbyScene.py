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
    
    def load(self):
        super().load()
        NetEvents.connector.client_init()

    def update_data(self):
        if self._session._state is not "needsPlayers":
            self.scenemanager.load_scene("GameScene")
            return
        self.image.fill(0)
        y = 0
        for player in self._session._players.values():
            nametag = self.font.render(player.name, True, player.color)
            self.image.blit(nametag, (100, 100+y))
            y += 100
