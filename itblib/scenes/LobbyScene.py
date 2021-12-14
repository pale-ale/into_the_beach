from typing import Generator

import pygame
import pygame.font
import pygame.surface
from itblib.Game import Session
from itblib.globals.Colors import BLACK
from itblib.net.NetEvents import NetEvents
from itblib.SceneManager import SceneManager
from itblib.scenes.SceneBase import SceneBase


class LobbyScene(SceneBase):
    def __init__(self, scenemanager: "SceneManager", session:"Session") -> None:
        super().__init__(scenemanager)
        self._session = session
        self.font = pygame.font.SysFont("latinmodernmono", 20)
        self.loaded_gamescene = False
        self.image = pygame.surface.Surface(scenemanager.scene_size)
        self.image.fill(BLACK)
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
    
    def load(self):
        super().load()
        self.loaded_gamescene = False
        NetEvents.connector.client_init()

    def update_data(self):
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
        header = self.font.render(f"Waiting for players ({len(self._session._players)}/2)...", True, (100,255,255,255))
        self.image.blit(header, (self.image.get_width()/2-header.get_width()/2, 50))
        for player in self._session._players.values():
            nametag = self.font.render(player.name.ljust(45) + "LVL: "+str(player.level).zfill(3), True, player.color, (100,100,100,255))
            self.image.blit(nametag, (100, 100+y))
            y += 100
        self.blits.append((self.image, self.image.get_rect(), self.image.get_rect()))

    def handle_key_event(self, keyevent):
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                NetEvents.snd_netplayerleave([p for p in self._session._players.values() if p.localcontrol][0])
                self.scenemanager.load_scene("MainMenuScene")
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits
