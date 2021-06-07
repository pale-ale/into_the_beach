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
from Maps import MapGrasslands

BLACK = [0, 0, 0] 
GREEN = [0, 255, 0]
RED = [255, 0, 0]
FPS = 30

pygame.display.init()
pygame.display.set_caption("Into The Bleach (for covid purposes only)")
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)

BACKGROUND = pygame.Surface((info.current_w, info.current_w))
BACKGROUND.fill((70,20,20))

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

grid = Grid.Grid()
gridui = GridUI.GridUI(grid)
gridui.load_map(MapGrasslands())
gridui.redraw_grid()
sprites.add(gridui)
running = True
lasttime = 0

while running:
    dt = clock.tick(FPS)/1000.0
    gridui.tick(dt)
    screen.blit(BACKGROUND, (0,0))
    pygame.transform.scale(gridui.image,(info.current_w,info.current_h), screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_t:
                gridui.grid.units[gridui.grid.width*9+9].attack([9,8],5)
    pygame.display.update()
pygame.quit()
