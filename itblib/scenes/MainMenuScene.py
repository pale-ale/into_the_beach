from itblib.SceneManager import SceneManager
import pygame
import pygame.font
from itblib.scenes.SceneBase import SceneBase

class MainMenuScene(SceneBase):
    """Main menu placeholder."""
    def __init__(self, scenemanager:"SceneManager", width: int, height: int, *groups) -> None:
        super().__init__(scenemanager, width, height, *groups)
        self.titlefont = pygame.font.SysFont('latinmodernmono', 50)
        self.subfont = pygame.font.SysFont('latinmodernmono', 20)
        x = self.titlefont.render("Wildes Main Menu", False, (50,200,150,255))
        y = self.subfont.render("ESC to quit, SPACE to queue", True, (50,200,150,255))
        self.image.blit(x, (100,100))
        self.image.blit(y, (100,300))
    
    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                exit(0)
            elif keyevent.key == pygame.K_SPACE:
                self.scenemanager.load_scene("GameScene")

    