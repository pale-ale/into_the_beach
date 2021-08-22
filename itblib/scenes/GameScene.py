from itblib.SceneManager import SceneManager
from itblib.Game import Session
from itblib.Grid import Grid
from itblib.net.Connector import Connector
from itblib.scenes.SceneBase import SceneBase
from itblib.Selector import Selector
from itblib.ui.GridUI import GridUI
from itblib.ui.HUD import Hud
from itblib.net.NetEvents import NetEvents
import pygame
import pygame.surface
import pygame.transform

class GameScene(SceneBase):
    """Contains the main game (grid, hud, etc.)"""
    def __init__(self, scenemanager:SceneManager, width: int, height: int) -> None:
        super().__init__(scenemanager, width, height)
        self.connector = Connector(False)
        self.session = Session(self.connector)
        self.grid = Grid(self.connector)
        self.gridui = GridUI(self.grid)
        self.grid.update_observer(self.gridui) 
        self.hud = Hud(width, height, self.gridui, 0, self.session)
        self.selector = Selector(self.grid, self.hud)
        self.griddisplaysize = (1280, 984)
        self.griduiscaleimage = pygame.Surface(self.griddisplaysize, pygame.SRCALPHA).convert_alpha()

    def load(self):
        super().load()
        self.connector.client_init()

    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.mod & pygame.KMOD_SHIFT and keyevent.key == pygame.K_UP:
                self.gridui.update_pan((self.gridui.pan[0], self.gridui.pan[1] + 2*22*self.hud.displayscale))
                return
            if keyevent.mod & pygame.KMOD_SHIFT and keyevent.key == pygame.K_DOWN:
                self.gridui.update_pan((self.gridui.pan[0], self.gridui.pan[1] - 2*22*self.hud.displayscale))
                return
        self.selector.handle_input(keyevent)

    def update(self, dt:float):
        super().update(dt)
        data = self.connector.receive()
        if data:
            prefix, contents = data
            NetEvents.rcv_event_caller(prefix, contents)
        self.image.fill((0,0,0,0))
        self.hud.redraw()
        self.grid.tick(dt)
        self.gridui.update()
        self.image.blit(self.hud.background, (0,0))
        pygame.transform.scale(self.gridui.image, self.griduiscaleimage.get_size(), self.griduiscaleimage)
        self.image.blit(self.griduiscaleimage, self.gridui.rect.topleft)
        self.image.blit(self.hud.image, (0,0))
