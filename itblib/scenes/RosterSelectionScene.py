from itblib.Globals.Enums import UNIT_IDS
from itblib.Globals.GridElementFactory import GridElementFactory
from itblib.ui.TextureManager import Textures
from pygame.surface import Surface
from itblib.Vec import Vec
from itblib.SceneManager import SceneManager
from itblib.scenes.SceneBase import SceneBase
from itblib.Player import PlayerData
import pygame
import pygame.font
import pygame.transform
import pygame.draw
import itblib.gridelements.units.Units as Units
import json
import sys

class RosterSelectionScene(SceneBase):
    """The user can select his lineup here."""
    def __init__(self, scenemanager:"SceneManager", width: int, height: int) -> None:
        super().__init__(scenemanager, width, height)
        self.playerfilepath = sys.argv[1]
        self.titlefont = pygame.font.SysFont('latinmodernmono', 50)
        self.subfont = pygame.font.SysFont('latinmodernmono', 20)
        t = self.titlefont.render("Select your lineup here.", True, (50,200,150,255))
        esctext = self.subfont.render(
            "ESC to quit, SPACE to save when 3(1) units have been selected, \
             ENTER to add/remove unit", True, (50,200,150,255))
        self.image.blit(t, (width*.5 - t.get_width()*.5, 20))
        self.image.blit(esctext, (width*.5 - esctext.get_width()*.5, 55))
        self.unitids = [1, 2, 3, 5, 6]
        self.unitlist = Surface((width, 400)).convert_alpha()
        self.tilewidth = 128
        self.tilemarginx = 3
        self.cursorpos = [0,0]
        self.tileheight = 128
        self.tilemarginy = 3
        self.maxnumberunits = 3
        self.tilecountline = 7 #int(width / (self.tilewidth + self.tilemarginx))
        freespace = width - self.tilecountline*self.tilewidth
        self.xspacer = int(freespace / (self.tilecountline+1))
        self.lines = 3
        self.selects = [False for i in range(self.lines*self.tilecountline)]
        for y in range(self.lines):
            for x in range(self.tilecountline):
                self.unitlist.fill(
                    (int(x/self.tilecountline*255), int(y/self.lines*255), 100, 255),
                    (*self.c_to_s((x,y)), self.tilewidth, self.tileheight)
                )
                unitindex = y*self.tilecountline+x
                if unitindex+1 < len(self.unitids):
                    tex = Surface((64,64)).convert_alpha()
                    t = Textures.get_spritesheet(
                        UNIT_IDS[unitindex+1]+"SWIdle"
                    )[0]
                    tex.blit(t, (0,0,64,64))
                    s = Surface((self.tilewidth, self.tileheight)).convert_alpha()
                    pygame.transform.scale(tex, s.get_size(), s)
                    self.unitlist.blit(s, self.c_to_s((x,y)))
                self.draw_tangle((x,y))
        self.image.blit(self.unitlist, (0, 100))
        self.update_cursor_pos((0,0))
    
    def update_cursor_pos(self, delta:"tuple[int,int]"):
        x,y = Vec.comp_add2(self.cursorpos, delta)
        self.cursorpos[0] = max(min(x,self.tilecountline), 0)
        self.cursorpos[1] = max(min(y,self.lines), 0)
        rect = (
            self.xspacer+x*(self.xspacer+self.tilewidth),  
            y*(self.tileheight+self.tilemarginy)+100, 
            self.tilewidth, 
            self.tileheight
        )
        self.image.blit(self.unitlist, (0, 100))
        pygame.draw.rect(self.image, (255, 50, 150), rect, 2, 5)
    
    def c_to_s(self, c:"tuple[int,int]"):
        x,y = c
        s = (self.xspacer+x*(self.xspacer+self.tilewidth),  y*(self.tileheight+self.tilemarginy))
        return s
    
    def draw_tangle(self, c:"tuple[int,int]", green:bool=False):
        verts = [Vec.comp_add2(x, self.c_to_s(c)) for x in ((118,0),(128,0),(128,10))]

        pygame.draw.polygon(
            self.unitlist,
            (0,255,0) if green else (150,150,150), 
            verts
        )
        self.image.blit(self.unitlist, (0, 100))

    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
            elif keyevent.key == pygame.K_SPACE:
                self.scenemanager.load_scene("GameScene")
            elif keyevent.key == pygame.K_RETURN:
                i = self.cursorpos[1]*self.tilecountline+self.cursorpos[0]
                self.selects[i] += 1
                self.draw_tangle(self.cursorpos, self.selects[i])
                self.update_cursor_pos((0,0))
                if sum(self.selects) == self.maxnumberunits:
                    self.units_selected(self.selects)
            elif keyevent.key == pygame.K_BACKSPACE:
                i = self.cursorpos[1]*self.tilecountline+self.cursorpos[0]
                if self.selects[i] > 0:
                    self.selects[i] -= 1
                    self.draw_tangle(self.cursorpos, self.selects[i])
                    self.update_cursor_pos((0,0))
            elif keyevent.key == pygame.K_UP:
                self.update_cursor_pos((0,-1))
            elif keyevent.key == pygame.K_RIGHT:
                self.update_cursor_pos((1,0))
            elif keyevent.key == pygame.K_DOWN:
                self.update_cursor_pos((0,1))
            elif keyevent.key == pygame.K_LEFT:
                self.update_cursor_pos((-1,0))

    def units_selected(self, selects):
        initialunits = []
        for index in range(len(selects)):
            for i in range(selects[index]):
                initialunits.append(self.unitids[index])
        PlayerData.load(self.playerfilepath)
        PlayerData.roster = initialunits
        PlayerData.save(self.playerfilepath)
        self.scenemanager.load_scene("GameScene")
