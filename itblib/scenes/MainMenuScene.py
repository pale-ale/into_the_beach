from itblib.SceneManager import SceneManager
import pygame
import pygame.font
from itblib.scenes.SceneBase import SceneBase

class MainMenuScene(SceneBase):
    """Main menu placeholder."""
    def __init__(self, client, scenemanager:"SceneManager", width: int, height: int, *groups) -> None:
        super().__init__(scenemanager, width, height, *groups)
        self.client = client
        self.titlefont = pygame.font.SysFont('latinmodernmono', 50)
        self.subfont = pygame.font.SysFont('latinmodernmono', 20)
        x = self.titlefont.render("Wildes Main Menu", False, (50,200,150,255))
        s = self.subfont.render("Settings", True, (50,200,150,255))
        s1 = self.subfont.render("      F: Toggle Fullscreen", True, (50,200,150,255))
        s2 = self.subfont.render("      Another great setting.", True, (50,200,150,255))
        y = self.subfont.render("ESC to quit, SPACE to queue", True, (50,200,150,255))
        self.image.blit(x, (100,100))
        self.fullscreen = False
        self.image.blit(s, (100,200))
        self.image.blit(s1, (100,230))
        self.image.blit(s2, (100,250))
        self.image.blit(y, (100,300))
    
    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                exit(0)
            elif keyevent.key == pygame.K_SPACE:
                self.scenemanager.load_scene("GameScene")
            elif keyevent.key == pygame.K_f:
                self.fullscreen = not self.fullscreen
                self.client.update_fullscreen(self.fullscreen)
    