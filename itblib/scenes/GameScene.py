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
    def __init__(self, scenemanager:SceneManager, width: int, height: int, *groups) -> None:
        super().__init__(scenemanager, width, height, *groups)
        self.connector = Connector(False)
        self.session = Session(self.connector)
        self.grid = Grid(self.connector)
        self.gridui = GridUI(self.grid)
        self.grid.update_observer(self.gridui) 
        self.hud = Hud(self.gridui.width, self.gridui.height, self.gridui, 0, self.session)
        self.scaleimage = pygame.Surface((self.gridui.width, self.gridui.height))
        self.selector = Selector(self.grid, self.hud)

    def load(self):
        super().load()
        self.connector.client_init()

    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        self.selector.handle_input(keyevent)

    def tick(self, dt:float):
        super().tick(dt)
        data = self.connector.receive()
        if data:
            prefix, contents = data
            NetEvents.rcv_event_caller(prefix, contents)
        
        self.image.fill((0,0,0,0))
        self.hud.redraw()
        self.scaleimage.blit(self.hud.background, (0,0))
        self.gridui.tick(dt)
        self.gridui.redraw_grid()
        self.scaleimage.blit(self.gridui.image, (0,0))
        self.scaleimage.blit(self.hud.image, (0,0))
        pygame.transform.scale(self.scaleimage, self.desired_size, self.image)
