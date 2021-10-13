from itblib.scenes.SceneBase import SceneBase
from itblib.SceneManager import SceneManager
from itblib.ui.TextBox import TextBox

import pygame
import pygame.font
import pygame.image
import pygame.transform

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
        s2 = self.subfont.render("      R: Edit Roster", True, (50,200,150,255))
        s3 = self.subfont.render("      M: Mapselection.", True, (50,200,150,255))
        bg = pygame.image.load("sprites/Splashscreen.png").convert_alpha()
        pygame.transform.scale(bg, self.image.get_size(), self.image).convert_alpha()
        self.image.blit(x, (100,100))
        self.tb1 = TextBox((100,30), "↑ Battle", fontsize=20)
        self.tb2 = TextBox((175,30), "→ Game Settings", fontsize=20)
        self.tb3 = TextBox((100,30), "Loadout ←", fontsize=20)
        self.tb4 = TextBox((100,30), "↓ Exit", fontsize=20)
        self.fullscreen = False
        self.image.blit(s, (100,200))
        self.image.blit(s1, (100,230))
        self.image.blit(s2, (100,250))
        self.image.blit(s3, (100,270))
        self.image.blit(self.tb1.image, (597,510))
        self.image.blit(self.tb2.image, (630,540))
        self.image.blit(self.tb3.image, (500,540))
        self.image.blit(self.tb4.image, (597,570))
    
    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                exit(0)
            elif keyevent.key == pygame.K_UP:
                self.scenemanager.load_scene("LobbyScene")
            elif keyevent.key == pygame.K_r:
                self.scenemanager.load_scene("RosterSelectionScene")
            elif keyevent.key == pygame.K_m:
                self.scenemanager.load_scene("MapSelectionScene")
            elif keyevent.key == pygame.K_f:
                self.fullscreen = not self.fullscreen
                self.client.update_fullscreen(self.fullscreen)
    