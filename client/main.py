import HUD 
import socket
import pygame
from pygame import display
from Selector import Selector
from TextureManager import Textures
from GridUI import GridUI
from Grid import Grid

FPS = 30

pygame.display.init()
pygame.font.init()
pygame.display.set_caption("Into The Bleach (for covid purposes only)")
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)

Textures.load_textures()

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

clientgrid = Grid()
clientgridui = GridUI(clientgrid)
clientgrid.update_observer(clientgridui)
hud = Hud(clientgridui.width, clientgridui.height, clientgridui)
selector = Selector(clientgrid, hud)

clientgridui.redraw_grid()
sprites.add(clientgridui)

camera = pygame.Surface((clientgridui.width, clientgridui.height))

hud.redraw()
running = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("nani?")
    s.connect(('127.0.0.1', 13579))
    s.send("Hello".encode("utf8"))
    while running:
        dt = clock.tick(FPS)/1000.0
        clientgridui.tick(dt)
        camera.blit(hud.background, (0,0))
        camera.blit(clientgridui.image, (0,0))
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



