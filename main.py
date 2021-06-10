import pygame
import pygame.sprite
import pygame.time
import pygame.transform
import pygame.display

import Effects
import Grid
import GridUI
import Tiles
import Units
from HUD import Hud
from Maps import MapGrasslands
from Selector import Selector

BLACK = [0, 0, 0] 
GREEN = [0, 255, 0]
RED = [255, 0, 0]
FPS = 30

pygame.display.init()
pygame.display.set_caption("Into The Bleach (for covid purposes only)")
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)

BACKGROUND = pygame.Surface((info.current_w, info.current_h))
BACKGROUND.fill((70,20,20))

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

grid = Grid.Grid()
gridui = GridUI.GridUI(grid)
hud = Hud(gridui.width, gridui.height, gridui)
grid.update_observer(gridui)
selector = Selector(grid, hud)

grid.load_map(MapGrasslands())
gridui.redraw_grid()
sprites.add(gridui)
running = True
lasttime = 0

while running:
    dt = clock.tick(FPS)/1000.0
    gridui.tick(dt)
    screen.blit(BACKGROUND, (0,0))
    cursorPos = gridui.transform_grid_screen(*selector.cursorposition)
    gridui.image.blit(hud.image, (0, 0))
    # TODO: move next line into HUD.py
    gridui.image.blit(gridui.uitiles[grid.c_to_i(*selector.cursorposition)].image, (gridui.width*.95, gridui.height*.9))

    pygame.transform.scale(gridui.image,(info.current_w,info.current_h), screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or pygame.KEYUP:
            selector.handle_input(event)
    pygame.display.update()
pygame.quit()
