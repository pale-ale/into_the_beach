from itblib.SceneManager import SceneManager
from itblib.Grid import Grid
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
        self.grid = Grid(NetEvents.connector)
        self.gridui = GridUI(self.grid)
        self.grid.update_observer(self.gridui) 
        self.hud = Hud(width, height, self.gridui, 0, NetEvents.session)
        self.selector = Selector(self.grid, self.hud)
        self.griddisplaysize = (1280, 984)
        self.griduiscaleimage = pygame.Surface(self.griddisplaysize, pygame.SRCALPHA).convert_alpha()
    
    def load(self):
        super().load()
        self.hud.on_start_game()

    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.mod & pygame.KMOD_SHIFT and keyevent.key == pygame.K_UP:
                self.gridui.update_pan((self.gridui.pan[0], self.gridui.pan[1] + 2*22*self.hud.displayscale))
                self.selector.move_cursor((-1,-1))
                return
            if keyevent.mod & pygame.KMOD_SHIFT and keyevent.key == pygame.K_DOWN:
                self.gridui.update_pan((self.gridui.pan[0], self.gridui.pan[1] - 2*22*self.hud.displayscale))
                self.selector.move_cursor((1,1))
                return
        self.selector.handle_input(keyevent)

    def update(self, dt:float):
        super().update(dt)
        self.image.fill((0,0,0,0))
        self.hud.redraw(dt)
        self.grid.tick(dt)
        self.gridui.update(dt)
        self.image.blit(self.hud.background, (0,0))
        pygame.transform.scale(self.gridui.image, self.griduiscaleimage.get_size(), self.griduiscaleimage)
        self.image.blit(self.griduiscaleimage, self.gridui.rect.topleft)
        self.image.blit(self.hud.image, (0,0))
