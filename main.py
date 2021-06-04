import pygame
import pygame.sprite
import pygame.time
import pygame.transform
import pygame.display

import Effects
import Grid
import GridUI
import Tiles

BLACK = [0, 0, 0] 
GREEN = [0, 255, 0]
RED = [255, 0, 0]
FPS = 30


pygame.display.init()
pygame.display.set_caption("Into The Bleach (for covid purposes only)")
info = pygame.display.Info()
print(info.current_w, info.current_h)
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)

BACKGROUND = pygame.Surface((info.current_w, info.current_w))
BACKGROUND.fill((70,20,20))

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

grid = Grid.Grid()
gridui = GridUI.GridUI(grid)
gridui.add_tile(0,0)
gridui.add_tile(0,9)
gridui.add_tile(9,9)
gridui.add_tile(9,0)
gridui.add_effect(0,0, effecttype=Effects.EffectFire)
gridui.add_effect(9,0, effecttype=Effects.EffectFire)
gridui.add_unit(0,9)

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
    pygame.display.update()
pygame.quit()
