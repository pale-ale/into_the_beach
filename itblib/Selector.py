import pygame

from itblib.Grid import Grid
from itblib.input.Input import InputAcceptor
from itblib.Log import log
from itblib.ui.hud.HUD import Hud
from itblib.Vec import add


class Selector(InputAcceptor):
    """A controller used to handle the player's input."""
    _instance:"Selector" = None

    @staticmethod
    def get_instance() -> "Selector":
        if Selector._instance:
            return Selector._instance
        Selector._instance = Selector()
        return Selector._instance

    def __init__(self, grid:Grid, hud:Hud):
        super().__init__()
        if self._instance:
            log("Selector: May only be initialized once.", 2)
        self.grid = grid
        self.hud = hud
        self.cursorposition = (0,0)
        self.hud.update_cursor(self.cursorposition)
        self._instance = self

    def move_cursor(self, delta:tuple[int,int]) -> bool:
        """Try moving cursor by delta. If it fails, return False.
        @delta: The amount in grid coordinates to move by."""
        testpos = add(self.cursorposition, delta)
        if self.grid.is_coord_in_bounds(testpos):
            self.cursorposition = testpos
            self.hud.update_cursor(self.cursorposition)
            return True
        return False

    def handle_key_event(self, event: any) -> bool:
        if super().handle_key_event(event):
            return True
        if event.type == pygame.KEYDOWN:
            # active abilities
            if event.unicode and event.unicode in "1234":
                self.hud.activate_ability(int(event.unicode))
                return True
            if not event.mod & pygame.KMOD_SHIFT:
            # navigate the grid
                delta = (0,0)
                if event.key == pygame.K_UP:
                    delta = (-1,0)
                elif event.key == pygame.K_RIGHT:
                    delta = (0,1)
                elif event.key == pygame.K_DOWN:
                    delta = (1,0)
                elif event.key == pygame.K_LEFT:
                    delta = (0,-1)
                if delta != (0,0):
                    self.move_cursor(delta)
                return delta != (0,0)
        return False
