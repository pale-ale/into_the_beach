import pygame
import pygame.sprite
import pygame.time
import pygame.transform
import pygame.display
import pygame.font

import Effects
import Grid
import GridUI
import Tiles
import Units
from Globals import Textures
from HUD import Hud
from Maps import MapGrasslands
from Selector import Selector


BLACK = [0, 0, 0] 
GREEN = [0, 255, 0]
RED = [255, 0, 0]
FPS = 30

pygame.display.init()
pygame.font.init()
pygame.display.set_caption("Into The Bleach (for covid purposes only)")
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)

Textures.load_textures()


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

BACKGROUND = pygame.Surface((gridui.width, gridui.height))
BACKGROUND.fill((70,20,20))
camera = pygame.Surface((gridui.width, gridui.height))

hud.redraw()
running = True
lasttime = 0

while running:
    dt = clock.tick(FPS)/1000.0
    gridui.tick(dt)
    camera.blit(gridui.image, (0,0))
    camera.blit(hud.image, (0,0))
    pygame.transform.scale(camera,(info.current_w,info.current_h), screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or pygame.KEYUP:
            selector.handle_input(event)
    pygame.display.update()
pygame.quit()
