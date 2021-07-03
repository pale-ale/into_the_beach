import pygame
import pygame.sprite
import pygame.time
import pygame.transform
import pygame.display
import pygame.font

from itblib.ui.GridUI import GridUI
from itblib.ui.HUD import Hud
from itblib.Selector import Selector
from itblib.Player import Player
from itblib.Game import Game
from itblib.ui.TextureManager import Textures


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

player1 = Player(12, None)
player2 = Player(13, None)
game = Game()
newsession = game.create_session()
newsession.add_player(player1)
newsession.add_player(player2)
gridui = GridUI(newsession._grid)
newsession._grid.update_observer(gridui)
newsession.start_game()

hud = Hud(gridui.width, gridui.height, gridui, player1.playerid, newsession)
selector = Selector(newsession._grid, hud)

gridui.redraw_grid()
sprites.add(gridui)

camera = pygame.Surface((gridui.width, gridui.height))

hud.redraw()
running = True

while running:
    dt = clock.tick(FPS)/1000.0
    gridui.tick(dt)
    camera.blit(hud.background, (0,0))
    camera.blit(gridui.image, (0,0))
    hud.tick(dt)
    hud.redraw()
    camera.blit(hud.image, (0,0))
    pygame.transform.scale(camera,(info.current_w,info.current_h), screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or pygame.KEYUP:
            selector.handle_input(event)
    pygame.display.update()
pygame.quit()
