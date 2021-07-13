import pygame
from pygame.constants import NOEVENT
import pygame.display
from itblib.scenes.GameScene import GameScene
from itblib.scenes.MainMenuScene import MainMenuScene
from itblib.SceneManager import SceneManager
from itblib.Selector import Selector
from itblib.ui.TextureManager import Textures
from itblib.net.NetEvents import NetEvents

FPS = 30

pygame.display.init()
pygame.font.init()
pygame.display.set_caption("Into The Bleach (for covid purposes only)")
info = pygame.display.Info()
DISPLAYSIZE = (int(info.current_w/2), int(info.current_h/2))
screen = pygame.display.set_mode(DISPLAYSIZE)
# screen = pygame.display.set_mode(DISPLAYSIZE, pygame.NOFRAME)

Textures.load_textures()

clock = pygame.time.Clock()

scenemanager = SceneManager()
mainmenuscene = MainMenuScene(scenemanager, *DISPLAYSIZE)
gamescene = GameScene(scenemanager, *DISPLAYSIZE)
NetEvents.grid = gamescene.grid
NetEvents.connector = gamescene.connector
NetEvents.session = gamescene.session
NetEvents.hud = gamescene.hud
selector = Selector(gamescene.grid, gamescene.hud)
scenemanager.add_scene("GameScene", gamescene)
scenemanager.add_scene("MainMenuScene", mainmenuscene)
gamescene = None
mainmenuscene = None
#scenemanager.load_scene("GameScene")
scenemanager.load_scene("MainMenuScene")

camera = pygame.Surface(DISPLAYSIZE)

running = True

while running:
    
    dt = clock.tick(FPS)/1000.0
    scenemanager.activescene.tick(dt)
    camera.blit(scenemanager.activescene.image, (0,0))
    pygame.transform.scale(camera, DISPLAYSIZE, screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or pygame.KEYUP:
            scenemanager.activescene.on_keyevent(event)
    pygame.display.update()
pygame.quit()
