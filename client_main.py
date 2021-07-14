import pygame
from pygame.constants import NOEVENT
import pygame.display
from itblib.scenes.GameScene import GameScene
from itblib.scenes.MainMenuScene import MainMenuScene
from itblib.SceneManager import SceneManager
from itblib.Selector import Selector
from itblib.ui.TextureManager import Textures
from itblib.net.NetEvents import NetEvents

class Client:
    def __init__(self) -> None:
        self.fps_cap = 30
        self.reference_displaysize = (1600, 900)
        #self.reference_displaysize = (1920, 1080)
        self.running = True

        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption("Into The Bleach (for covid purposes only)")
        self.displayinfo = pygame.display.Info()
        self.displaysize = (int(self.displayinfo.current_w), int(self.displayinfo.current_h))
        self.displayscale = (self.displaysize[0]/self.reference_displaysize[0],
                             self.displaysize[1]/self.reference_displaysize[1])
        self.clock = pygame.time.Clock()
        self.displayscale = (self.displaysize[0]/self.reference_displaysize[0],
                             self.displaysize[1]/self.reference_displaysize[1])
        self.screen = pygame.display.set_mode(self.displaysize, pygame.RESIZABLE)
        #Textures.load_textures(DISPLAYSCALE)
        Textures.load_textures()
        self.scenemanager = SceneManager()
        mainmenuscene = MainMenuScene(self.scenemanager, *self.displaysize)
        gamescene = GameScene(self.scenemanager, *self.displaysize)
        NetEvents.grid = gamescene.grid
        NetEvents.connector = gamescene.connector
        NetEvents.session = gamescene.session
        NetEvents.hud = gamescene.hud
        self.selector = Selector(gamescene.grid, gamescene.hud)
        self.scenemanager.add_scene("GameScene", gamescene)
        self.scenemanager.add_scene("MainMenuScene", mainmenuscene)
        self.scenemanager.load_scene("MainMenuScene")
        self.camera = pygame.Surface(self.displaysize)

    def reload_textures(self):
        self.displayinfo = pygame.display.Info()
        self.displaysize = (int(self.displayinfo.current_w), int(self.displayinfo.current_h))
        self.displayscale = (self.displaysize[0]/self.reference_displaysize[0],
                        self.displaysize[1]/self.reference_displaysize[1])
        Textures.load_textures(self.displayscale)
        self.scenemanager.scenes["GameScene"].on_displayresize(self.displayscale)

client = Client()

sampleimage = pygame.image.load("./sprites/TileDirtDefault0.png")

while client.running:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            client.reload_textures()
        if event.type == pygame.QUIT:
            client.running = False
        if event.type == pygame.KEYDOWN or pygame.KEYUP:
            client.scenemanager.activescene.on_keyevent(event)
    dt = client.clock.tick(client.fps_cap)/1000.0
    client.scenemanager.activescene.tick(dt)
    client.screen.blit(client.scenemanager.activescene.image, (0,0))
    client.screen.blit(sampleimage, (400,400))
    #pygame.transform.scale(camera, DISPLAYSIZE, screen)
    pygame.display.update()
pygame.quit()
