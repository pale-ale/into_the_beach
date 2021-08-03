import pygame

from itblib.ui.HUD import Hud 
from itblib.Grid import Grid

class Selector:
    """A controller used to handle the player's input."""

    def __init__(self, grid:Grid, hud:Hud):
        self.grid = grid
        self.cursorposition = (int(),int())
        self.hud = hud
        self.hud.update_cursor(self.cursorposition)

    def add(self, a:"tuple[int,int]", b:"tuple[int,int]"):
        """Add two 2d-vectors."""
        return a[0] + b[0], a[1] + b[1]
    
    def handle_input(self, event):
        """Manages pygame's key-events and forwards them to e.g. the HUD."""
        if event.type == pygame.KEYDOWN:
            # exit game
            if event.key == pygame.K_ESCAPE:
                self.hud.escape_pressed()
            if event.key == pygame.K_SPACE:
                self.hud.unitselect(self.cursorposition)
                return
            if event.key == pygame.K_RETURN:
                self.hud.targetselect(self.cursorposition)
                return

            # active abilities
            if event.unicode and event.unicode in "1234":
                self.hud.activate_ability(int(event.unicode))
                return

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
            testpos = self.add(self.cursorposition, delta)
            if self.grid.is_coord_in_bounds(testpos):
                self.cursorposition = testpos
                self.hud.update_cursor(testpos)
            return
