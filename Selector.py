from typing import Text
import pygame

class Selector:
    def __init__(self, grid, hud):
        self.grid = grid
        self.up = False
        self.left = False
        self.down = False
        self.right = False
        self.cursorposition = [0,0]
        self.hud = hud

    def add(self, a, b):
        return a[0] + b[0], a[1] + b[1]
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_SPACE:
                self.hud.select(self.cursorposition)
                return
            # navigate the grid
            elif event.key == pygame.K_UP:
                self.up = True
            elif event.key == pygame.K_LEFT:
                self.left = True
            elif event.key == pygame.K_DOWN:
                self.right = True
            elif event.key == pygame.K_RIGHT:
                self.down = True
            return
        
        elif event.type == pygame.KEYUP:
            delta = (0,0)
            if event.key == pygame.K_SPACE:
                return
            # navigate the grid
            elif event.key == pygame.K_UP:
                self.up = False
                delta = (-1,0)
            elif event.key == pygame.K_LEFT:
                self.left = False
                delta = (0,-1)
            elif event.key == pygame.K_DOWN:
                self.right = False
                delta = (1,0)
            elif event.key == pygame.K_RIGHT:
                self.down = False
                delta = (0,1)

            testpos = self.add(self.cursorposition, delta)
            if self.grid.is_coord_in_bounds(*testpos):
                self.cursorposition = testpos
                self.hud.update_cursor(testpos)
            return
