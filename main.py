import pygame.time
import pygame.sprite
import pygame

import GridUI
import Grid
import Tiles
import Effects

WIDTH = 1000
HEIGHT = 700
BLACK = [0, 0, 0] 
GREEN = [0, 255, 0]
RED = [255, 0, 0]
FPS = 30

pygame.init()
pygame.display.set_caption("Into The Bleach (for covid purposes only)")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
world = pygame.surface.Surface((WIDTH,HEIGHT))

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

grid = Grid.Grid()
gridui = GridUI.GridUI(grid)
gridui.add_tile(0,1)
gridui.add_tile(0,2)
gridui.add_tile(0,3)
gridui.add_tile(0,4, tiletype=Tiles.TileSea)
gridui.add_tile(1,0, tiletype=Tiles.TileSea)
gridui.add_tile(2,0, tiletype=Tiles.TileSea)
gridui.add_tile(3,0, tiletype=Tiles.TileSea)
gridui.add_tile(4,0)
gridui.add_tile(3,4)
gridui.add_tile(4,3)
gridui.add_tile(5,8, tiletype=Tiles.TileSea)
gridui.add_tile(6,8, tiletype=Tiles.TileSea)
gridui.add_tile(7,8, tiletype=Tiles.TileSea)
gridui.add_tile(8,5, tiletype=Tiles.TileSea)
gridui.add_tile(8,6, tiletype=Tiles.TileSea)
gridui.add_tile(8,7, tiletype=Tiles.TileSea)
gridui.add_effect(0,1, effecttype=Effects.EffectFire)

gridui.redraw_grid()
sprites.add(gridui)
running = True
lasttime = 0

while running:
    dt = clock.tick(FPS)/1000.0
    gridui.tick(dt)
    world.fill((70,20,20))
    sprites.draw(world)
    screen.blit(world, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    pygame.display.flip()
pygame.quit()
