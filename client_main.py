import json
from itblib import Maps
import socket
import pygame
from pygame import display
from itblib.ui.HUD import Hud
from itblib.Selector import Selector
from itblib.ui.TextureManager import Textures
from itblib.ui.GridUI import GridUI
from itblib.Grid import Grid
from itblib.net.Connector import Connector

FPS = 30

pygame.display.init()
pygame.font.init()
pygame.display.set_caption("Into The Bleach (for covid purposes only)")
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)

Textures.load_textures()

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
connector = Connector(False)
connector.client_init()
data = connector.receive()
if data:
    prefix, contents = data
    if prefix == "MapTransfer":
        newmap = Maps.Map()
        obj = json.loads(contents)
        newmap.height = obj["height"]
        newmap.width = obj["width"]
        newmap.tileids = obj["tileids"]
        newmap.unitids = obj["unitids"]
        newmap.effectids = obj["effectids"]
        #if contents == "MapGrasslands":
        #    clientgrid.load_map(Maps.MapGrasslands())
clientgrid = Grid(width=newmap.width, height=newmap.height)
clientgridui = GridUI(clientgrid)
clientgrid.update_observer(clientgridui)
clientgrid.load_map(newmap)
hud = Hud(clientgridui.width, clientgridui.height, clientgridui)
selector = Selector(clientgrid, hud)

clientgridui.redraw_grid()
sprites.add(clientgridui)

camera = pygame.Surface((clientgridui.width, clientgridui.height))

hud.redraw()
running = True


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
