from itblib.scenes.SceneBase import SceneBase
from itblib.SceneManager import SceneManager
from itblib.ui.KeyIcon import KeyIcon
from itblib.ui.TextBox import TextBox

import pygame
import pygame.font
import pygame.image
import pygame.transform
import pygame.sprite
import random

class MainMenuScene(SceneBase):
    """Main menu placeholder."""
    def __init__(self, client, scenemanager:"SceneManager", width: int, height: int, *groups) -> None:
        super().__init__(scenemanager, width, height, *groups)
        self.fullscreen = False
        self.client = client
        self.bg = pygame.image.load("sprites/Splashscreen.png").convert_alpha()
        
        bgsprite = pygame.sprite.Sprite()
        bgsprite.image = pygame.Surface((width, height))
        bgsprite.rect = bgsprite.image.get_rect()
        self.bgsprites = pygame.sprite.Group(bgsprite)

        tb_title      = TextBox(text="Wildes Main Menu",  textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(150, 10), fontsize=30, )
        tb_subtitile  = TextBox(text="Settings:",         textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(150, 50))
        tb_fullscreen = TextBox(text="Toggle Fullscreen", textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(180,100))
        tb_roster     = TextBox(text="Edit Roster",       textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(155,150))
        tb_map        = TextBox(text="Mapselection.",     textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(130,200))
        tb_battle     = TextBox(text="Battle",            textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(width/2 - 26-32, height*.85))
        tb_settings   = TextBox(text="Game Settings",     textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(width/2 + 26+34, height*.9 ))
        tb_loadout    = TextBox(text="Loadout",           textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(width/2 - 26-86, height*.9 ))
        tb_exit       = TextBox(text="Exit",              textcolor=(50,255,255,255), bgcolor=(255,100,255,150), pos=(width/2 + 26+ 4, height*.95))
        
        self.textsprites = pygame.sprite.Group(
            tb_title, tb_subtitile, tb_fullscreen, tb_roster, tb_map,
            tb_battle, tb_settings, tb_loadout, tb_exit
        )

        ki_up    = KeyIcon('↑', size=(26,26), pos=(width/2   , height*.85))
        ki_left  = KeyIcon('←', size=(26,26), pos=(width/2-30, height*.9))
        ki_right = KeyIcon('→', size=(26,26), pos=(width/2+30, height*.9))
        ki_down  = KeyIcon('↓', size=(26,26), pos=(width/2   , height*.95))
        ki_f     = KeyIcon('F', size=(26,26), pos=(150, 100))
        ki_r     = KeyIcon('R', size=(26,26), pos=(125, 150))
        ki_m     = KeyIcon('M', size=(26,26), pos=(100, 200))

        self.keysprites = pygame.sprite.Group(
            ki_up, ki_left, ki_right, ki_down, 
            ki_f, ki_r, ki_m
        )

        self.lightspots:"list[tuple[int,int]]" = self._init_lightspots()
    
    def _init_lightspots(self):
        ls:"list[tuple[int,int]]" = []
        ls.extend([(x,y) for x in range( 45,  62, 3) for y in range (65, 112, 4)])
        ls.extend([(x,y) for x in range( 79,  89, 3) for y in range (85, 112, 4)])
        ls.extend([(x,y) for x in range(122, 135, 3) for y in range (42, 112, 4)])
        ls.extend([(x,y) for x in range(157, 175, 3) for y in range (42, 112, 4)])
        for spot in ls:
            self.bg.set_at(spot, (200,200,255,255) if random.randint(0,1) else (0))
        return ls
    
    def update(self, dt: float, debug=False):
        if debug:
            for spot in self.lightspots:
                self.bg.set_at(spot, (255,255,255,255))
        else:
            spot = self.lightspots[random.randrange(0, len(self.lightspots))]
            self.bg.set_at(spot, (200,200,255,255) if random.randint(0,1) else (0))
        pygame.transform.scale(self.bg, self.bgsprites.sprites()[0].image.get_size(), self.bgsprites.sprites()[0].image).convert_alpha()
        self.bgsprites.draw(self.image)
        self.textsprites.draw(self.image)
        self.keysprites.draw(self.image)
        return super().update(dt)
    
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
    