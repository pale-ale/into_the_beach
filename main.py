import pygame.time
import pygame.sprite
import pygame

import GridUI
import Grid

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
grid.add_tile(0,1)
grid.add_tile(0,2)
grid.add_tile(0,3)
grid.add_tile(0,4, tiletype=Grid.TileSea)
grid.add_tile(1,0, tiletype=Grid.TileSea)
grid.add_tile(2,0, tiletype=Grid.TileSea)
grid.add_tile(3,0, tiletype=Grid.TileSea)
grid.add_tile(4,0)
grid.add_tile(3,4)
grid.add_tile(4,3)
grid.add_tile(5,8, tiletype=Grid.TileSea)
grid.add_tile(6,8, tiletype=Grid.TileSea)
grid.add_tile(7,8, tiletype=Grid.TileSea)
grid.add_tile(8,5, tiletype=Grid.TileSea)
grid.add_tile(8,6, tiletype=Grid.TileSea)
grid.add_tile(8,7, tiletype=Grid.TileSea)

gridui = GridUI.GridUI(grid)
gridui.redraw_grid()
sprites.add(gridui)
running = True
while running:
    clock.tick(FPS)
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
