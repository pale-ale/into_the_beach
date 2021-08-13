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
    def __init__(self, griddisplaysize, scenemanager:SceneManager, width: int, height: int, *groups) -> None:
        super().__init__(scenemanager, width, height, *groups)
        self.connector = Connector(False)
        self.session = Session(self.connector)
        self.grid = Grid(self.connector)
        self.gridui = GridUI(self.grid)
        self.grid.update_observer(self.gridui) 
        self.hud = Hud(self.gridui.width, self.gridui.height, self.gridui, 0, self.session)
        self.selector = Selector(self.grid, self.hud)
        self.griddisplaysize = griddisplaysize 
        # self.griduiscaleimage = pygame.Surface(self.griddisplaysize, pygame.SRCALPHA).convert_alpha()
        self.griduiscaleimage = pygame.Surface((1260, 960), pygame.SRCALPHA).convert_alpha()
        self.hudscaleimage = pygame.Surface(self.desired_size, pygame.SRCALPHA).convert_alpha()

    def load(self):
        super().load()
        self.connector.client_init()

    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        self.selector.handle_input(keyevent)

    def on_displayresize(self, newsize:"tuple[int,int]"):
        self.hudscaleimage = pygame.Surface(newsize, pygame.SRCALPHA).convert_alpha()
        super().on_displayresize(newsize)

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
        pygame.transform.scale(self.hud.background, self.desired_size, self.image)
        pygame.transform.scale(self.gridui.image, self.griduiscaleimage.get_size(), self.griduiscaleimage)
        #self.griduiscaleimage.blit(self.gridui.image, (0,0))
        gridoffset = ((self.desired_size[0] - self.griddisplaysize[0])/2, (self.desired_size[1] - self.griddisplaysize[1])/2)
        self.image.blit(self.griduiscaleimage, gridoffset)
        pygame.transform.scale(self.hud.image, self.desired_size, self.hudscaleimage)
        self.image.blit(self.hudscaleimage, (0,0))
