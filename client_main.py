from itblib.Game import Session
import json
from itblib import Maps
import socket
import pygame
import itblib.net.NetEvents as NetEvents
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
DISPLAYSIZE = (int(info.current_w/2), int(info.current_h/2))
screen = pygame.display.set_mode(DISPLAYSIZE)
# screen = pygame.display.set_mode(DISPLAYSIZE, pygame.NOFRAME)

Textures.load_textures()

sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
connector = Connector(False)
connector.client_init()

clientgrid = Grid(connector)
clientsession = Session(connector)
NetEvents.StaticObjects["Grid"] = clientgrid
NetEvents.StaticObjects["Connector"] = connector
NetEvents.StaticObjects["Session"] = clientsession
clientgridui = GridUI(clientgrid)
clientgrid.update_observer(clientgridui)
hud = Hud(clientgridui.width, clientgridui.height, clientgridui, 0, clientsession)
NetEvents.StaticObjects["Hud"] = hud
selector = Selector(clientgrid, hud)

clientgridui.redraw_grid()
sprites.add(clientgridui)

camera = pygame.Surface((clientgridui.width, clientgridui.height))

hud.redraw()
running = True

while running:
    data = connector.receive()
    if data:
        prefix, contents = data
        NetEvents.rcv_event_caller(prefix, contents)
    dt = clock.tick(FPS)/1000.0
    clientgridui.tick(dt)
    camera.blit(hud.background, (0,0))
    camera.blit(clientgridui.image, (0,0))
    hud.tick(dt)
    hud.redraw()
    camera.blit(hud.image, (0,0))
    pygame.transform.scale(camera, DISPLAYSIZE, screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or pygame.KEYUP:
            selector.handle_input(event)
    pygame.display.update()
pygame.quit()
