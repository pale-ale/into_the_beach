import pygame
import pygame.display
import pygame.time
from itblib.scenes.GameScene import GameScene
from itblib.scenes.MainMenuScene import MainMenuScene
from itblib.SceneManager import SceneManager
from itblib.Selector import Selector
from itblib.net.NetEvents import NetEvents
from itblib.ui.TextureManager import Textures

class Client:
    """The Client manages everything needed for a player on his machine, including graphics, the screen, etc."""
    def __init__(self) -> None:
        self.fps_cap = 30
        self.normal_displaysize = (1280, 960)
        self.displaysize = self.normal_displaysize
        self.running = True

        pygame.display.init()
        self.fullscreen_displaysize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        pygame.font.init()
        pygame.display.set_caption("Into The Bleach (for covid purposes only)")
        self.displayinfo = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.displaysize, pygame.NOFRAME)
        Textures.load_textures()
        self.scenemanager = SceneManager()
        mainmenuscene = MainMenuScene(self, self.scenemanager, *self.displaysize)
        gamescene = GameScene(self.normal_displaysize, self.scenemanager, *self.displaysize)
        NetEvents.grid = gamescene.grid
        NetEvents.connector = gamescene.connector
        NetEvents.session = gamescene.session
        NetEvents.hud = gamescene.hud
        self.selector = Selector(gamescene.grid, gamescene.hud)
        self.scenemanager.add_scene("GameScene", gamescene)
        self.scenemanager.add_scene("MainMenuScene", mainmenuscene)
        self.scenemanager.load_scene("MainMenuScene")

    def update_fullscreen(self, fullscreen:bool = False):
        #TODO: hud elements may also not be scaled up or down, only repositioned
        if fullscreen:
            self.screen = pygame.display.set_mode(self.fullscreen_displaysize, pygame.NOFRAME | pygame.FULLSCREEN)
            self.scenemanager.scenes["GameScene"].on_displayresize(self.fullscreen_displaysize)
        else:
            # this actually needs to be called 2 times for god knows why.
            self.scenemanager.scenes["GameScene"].on_displayresize(self.normal_displaysize)
            self.screen = pygame.display.set_mode(self.normal_displaysize, pygame.NOFRAME).convert_alpha()
            self.screen = pygame.display.set_mode(self.normal_displaysize, pygame.NOFRAME).convert_alpha()

client = Client()

while client.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client.running = False
        elif pygame.key.get_focused() and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
            client.scenemanager.activescene.on_keyevent(event)
    dt = client.clock.tick(client.fps_cap)/1000.0
    client.scenemanager.activescene.update(dt)
    client.screen.fill((0,0,0,0))
    client.screen.blit(client.scenemanager.activescene.image, (0,0))
    pygame.display.update()
pygame.quit()
