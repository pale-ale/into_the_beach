from typing import Generator

import pygame
from pygame.constants import K_ESCAPE
import pygame.surface
import pygame.transform
from itblib.globals.Enums import NORTH, SOUTH, EAST, WEST
from itblib.Grid import Grid
from itblib.net.NetEvents import NetEvents
from itblib.SceneManager import SceneManager
from itblib.scenes.SceneBase import SceneBase
from itblib.Selector import Selector
from itblib.ui.GridUI import GridUI
from itblib.ui.hud.HUD import Hud


class GameScene(SceneBase):
    """Contains the main game (grid, hud, etc.)"""
    def __init__(self, scenemanager:SceneManager) -> None:
        super().__init__(scenemanager)
        self.grid = Grid(NetEvents.connector)
        self.gridui = GridUI(self.grid)
        self.grid.update_observer(self.gridui) 
        self.hud = Hud(scenemanager.scene_size, self.gridui, 0, NetEvents.session)
        self.selector = Selector(self.grid, self.hud)
        self.register_input_listeners(self.selector, self.hud)
    
    def load(self):
        super().load()
        self.hud.on_start_game()

    def handle_key_event(self, event) -> bool:
        if super().handle_key_event(event):
            return True
        elif event.type == pygame.KEYDOWN:
            if event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_UP:
                self.gridui.update_pan((self.gridui._pan[0], self.gridui._pan[1] + 2*22*self.hud.displayscale))
                self.selector.move_cursor(SOUTH)
                self.selector.move_cursor(SOUTH)
                self.hud.update_cursor()
                return True
            elif event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_DOWN:
                self.gridui.update_pan((self.gridui._pan[0], self.gridui._pan[1] - 2*22*self.hud.displayscale))
                self.selector.move_cursor(NORTH)
                self.selector.move_cursor(NORTH)
                self.hud.update_cursor()
                return True
            elif event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_LEFT:
                self.gridui.update_pan((self.gridui._pan[0]+2*32*self.hud.displayscale, self.gridui._pan[1]))
                self.selector.move_cursor(EAST)
                self.selector.move_cursor(EAST)
                self.hud.update_cursor()
                return True
            elif event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_RIGHT:
                self.gridui.update_pan((self.gridui._pan[0]-2*32*self.hud.displayscale, self.gridui._pan[1]))
                self.selector.move_cursor(WEST)
                self.selector.move_cursor(WEST)
                self.hud.update_cursor()
                return True
            if event.key == K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
                return True
        return False

    def update(self, delta_time:float):
        super().update(delta_time)
        self.grid.tick(delta_time)
        self.gridui.update(delta_time)
        self.hud.update(delta_time)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits
        self.blits.clear()
        yield from self.gridui.get_blits()
        yield from self.hud.get_blits()
