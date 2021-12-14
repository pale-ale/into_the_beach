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
    def __init__(self, scenemanager:"SceneManager") -> None:
        super().__init__(scenemanager)
        self.bg = pygame.image.load("sprites/Splashscreen.png").convert_alpha()
        self.spottime = 0
        self.spotchangetime = .1
        
        width, height = self.bg.get_size()
        tb_fullscreen = TextBox(text="Toggle Fullscreen", textcolor=(50,255,255,255), fontsize=11, bgcolor=(255,100,255,150), pos=(350, 12))
        tb_map        = TextBox(text="Map Selection",     textcolor=(50,255,255,255), fontsize=11, bgcolor=(255,100,255,150), pos=(375, 37))
        tb_roster     = TextBox(text="Edit Roster",       textcolor=(50,255,255,255), fontsize=11, bgcolor=(255,100,255,150), pos=(400, 62))
        tb_battle     = TextBox(text="Battle",            textcolor=(50,255,255,255), fontsize=11, bgcolor=(255,100,255,150), pos=(width/2 - 26-15, height*.805))
        tb_settings   = TextBox(text="Game Settings",     textcolor=(50,255,255,255), fontsize=11, bgcolor=(255,100,255,150), pos=(width/2 + 26+29, height*.87))
        tb_loadout    = TextBox(text="Loadout",           textcolor=(50,255,255,255), fontsize=11, bgcolor=(255,100,255,150), pos=(width/2 - 26-52, height*.87))
        tb_exit       = TextBox(text="Exit",              textcolor=(50,255,255,255), fontsize=11, bgcolor=(255,100,255,150), pos=(width/2 + 25, height*.945))
        
        self.textsprites = [
            tb_fullscreen, tb_roster, tb_map,
            tb_battle, tb_settings, tb_loadout, tb_exit
        ]

        ki_up    = KeyIcon('↑', size=(26,26), pos=(width/2   , height*.8))
        ki_left  = KeyIcon('←', size=(26,26), pos=(width/2-30, height*.85))
        ki_right = KeyIcon('→', size=(26,26), pos=(width/2+30, height*.85))
        ki_down  = KeyIcon('↓', size=(26,26), pos=(width/2   , height*.9))
        ki_f     = KeyIcon('F', size=(26,26), pos=(325,   5))
        ki_m     = KeyIcon('M', size=(26,26), pos=(350,  30))
        ki_r     = KeyIcon('R', size=(26,26), pos=(375,  55))

        self.keysprites = [
            ki_up, ki_left, ki_right, ki_down, 
            ki_f, ki_r, ki_m
        ]
    
    def load(self):
        super().load()
        self.blits.append((self.bg, self.bg.get_rect(), self.bg.get_rect()))
        for k in self.keysprites:
            self.blits.append((k.image, k.rect, pygame.Rect(0,0,*k.rect.size)))
        for tb in self.textsprites:
            self.blits.append((tb.image, tb.rect, pygame.Rect(0,0,*tb.rect.size)))

        self.lightspots:"list[tuple[int,int]]" = self._get_lightspots()
        for i in range(len(self.lightspots)):
            self._set_light(i)
    
    def unload(self):
        return super().unload()
    
    def handle_key_event(self, event: any) -> bool:
        if super().handle_key_event(event):
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit(0)
                return True
            elif event.key == pygame.K_UP:
                self.scenemanager.load_scene("LobbyScene")
                return True
            elif event.key == pygame.K_r:
                self.scenemanager.load_scene("RosterSelectionScene")
                return True
            elif event.key == pygame.K_m:
                self.scenemanager.load_scene("MapSelectionScene")
                return True
            elif event.key == pygame.K_f:
                self.fullscreen = not self.fullscreen
                self.client.update_fullscreen(self.fullscreen)
                return True
        return False

    def _get_lightspots(self):
        ls:"list[tuple[int,int]]" = []
        ls.extend([(x,y) for x in range( 45,  62, 3) for y in range (65, 112, 4)])
        ls.extend([(x,y) for x in range( 79,  89, 3) for y in range (85, 112, 4)])
        ls.extend([(x,y) for x in range(122, 135, 3) for y in range (42, 112, 4)])
        ls.extend([(x,y) for x in range(157, 175, 3) for y in range (42, 112, 4)])
        return ls
    
    def _set_light(self, index:int, color:"tuple[int,int,int,int]|None"=None):
        pos = self.lightspots[index]
        if color:
            self.bg.set_at(pos, color)
        else:
            self.bg.set_at(pos, (200,200,255,255) if random.randint(0,1) else (0,0,0,255))
        self.blits.append((self.bg, pygame.Rect(*pos,1,1), pygame.Rect(*pos,1,1)))
    
    def update(self, dt: float, debug=False):
        self.spottime += dt
        if self.spottime > self.spotchangetime:
            self.spottime = 0
            if debug:
                for spot in self.lightspots:
                    self.bg.set_at(spot, (255,255,255,255))
            else:
                index = random.randrange(0, len(self.lightspots))
                self._set_light(index)
        return super().update(dt)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits
        self.blits.clear()
    