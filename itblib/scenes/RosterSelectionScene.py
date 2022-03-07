import sys
from typing import Generator

import pygame
import pygame.draw
import pygame.font
import pygame.transform
from itblib.globals.Colors import DARK_GRAY, GREEN, ORANGE, RED
from itblib.globals.Enums import UNIT_IDS
from itblib.Player import PlayerData
from itblib.SceneManager import SceneManager
from itblib.scenes.SceneBase import SceneBase
from itblib.ui.TextureManager import Textures
from itblib.Vec import add
from pygame.surface import Surface


class RosterSelectionScene(SceneBase):
    """The user can select his lineup here."""
    def __init__(self, scenemanager:"SceneManager", playerfilepath:"str") -> None:
        super().__init__(scenemanager)
        self.image = pygame.Surface(self.scenemanager.scene_size)
        self.playerfilepath = playerfilepath
        self.titlefont = pygame.font.SysFont('latinmodernmono', 50)
        self.subfont = pygame.font.SysFont('latinmodernmono', 20)
        t = self.titlefont.render("Select your lineup here.", True, (50,200,150,255))
        esctext = self.subfont.render(
            "ESC to quit, SPACE to save when 3 units have been selected, \
             ENTER to add/remove unit", True, (50,200,150,255))
        width = self.image.get_width()
        self.image.blit(t, (width*.5 - t.get_width()*.5, 20))
        self.image.blit(esctext, (width*.5 - esctext.get_width()*.5, 55))
        self.unitids = [1, 2, 3, 5, 6, 7, 8]
        self.unitlist = Surface((width, 400)).convert_alpha()
        self.tilewidth = 128
        self.tilemarginx = 3
        self.cursorpos = [0,0]
        self.tileheight = 128
        self.tilemarginy = 3
        self.maxnumberunits = 3
        self.tilecountline = int(width / (self.tilewidth + self.tilemarginx))
        freespace = width - self.tilecountline*self.tilewidth
        self.xspacer = int(freespace / (self.tilecountline+1))
        self.lines = 2
        self.MAX_SINGLE_UNIT_COUNT = 3
        self.screenmarginx = 2
        self.selects = [0 for i in range(self.lines*self.tilecountline)]
        self.label_offset = (0,100)
        for y in range(self.lines):
            for x in range(self.tilecountline):
                self.unitlist.fill(
                    (int(x/self.tilecountline*255), int(y/self.lines*255), 100, 255),
                    (*self.c_to_s((x,y)), self.tilewidth, self.tileheight)
                )
        for unitindex in range(len(self.unitids)):
            x = unitindex%self.tilecountline
            y = int(unitindex/self.tilecountline)
            tex = Surface((64,64)).convert_alpha()
            tex.fill((0))
            spritesheet = Textures.get_spritesheet(
                UNIT_IDS[self.unitids[unitindex]]+"SWIdle"
            )
            if spritesheet:
                t = spritesheet[0]
                tex.blit(t, (0,0,64,64))
            s = Surface((self.tilewidth, self.tileheight)).convert_alpha()
            pygame.transform.scale(tex, s.get_size(), s)
            self.unitlist.blit(s, self.c_to_s((x,y)))
            self.draw_tangle((x,y))
        self.image.blit(self.unitlist, (0, 100))
        self.update_cursor_pos((0,0))
    
    def update_cursor_pos(self, delta:"tuple[int,int]"):
        x,y = add(self.cursorpos, delta)
        self.cursorpos[0] = max(min(x,self.tilecountline-1), 0)
        self.cursorpos[1] = max(min(y,self.lines-1), 0)
        linewidth = 2
        rect = (
            add(add(self.c_to_s(self.cursorpos), self.label_offset), (-linewidth, -linewidth)),
            (self.tilewidth + 2*linewidth, self.tileheight+2*linewidth)
        )
        self.image.fill(0, (0,90,self.image.get_width(), 10))
        self.image.blit(self.unitlist, self.label_offset)
        pygame.draw.rect(self.image, (255, 50, 150), rect, linewidth, 5)
    
    def c_to_s(self, c:"tuple[int,int]"):
        x,y = c
        sx = self.screenmarginx + self.xspacer+x*(self.xspacer+self.tilewidth)
        sy = y*(self.tileheight+self.tilemarginy)
        return (sx, sy)
    
    def draw_tangle(self, c:"tuple[int,int]", count:int=0):
        tangle_size = 10
        verts = [add(x, self.c_to_s(c)) for x in ((self.tilewidth-tangle_size-1,0),(self.tilewidth-1,0),(self.tilewidth-1,tangle_size))]
        pygame.draw.polygon(self.unitlist, [DARK_GRAY, RED, ORANGE, GREEN][count], verts)
        self.image.blit(self.unitlist, self.label_offset)

    def handle_key_event(self, keyevent):
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
            elif keyevent.key == pygame.K_RETURN:
                i = self.cursorpos[1]*self.tilecountline+self.cursorpos[0]
                if self.selects[i] < self.MAX_SINGLE_UNIT_COUNT:
                    self.selects[i] += 1
                    self.draw_tangle(self.cursorpos, self.selects[i])
                    self.update_cursor_pos((0,0))
            elif keyevent.key == pygame.K_SPACE:
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
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.image, self.image.get_rect(), self.image.get_rect())
