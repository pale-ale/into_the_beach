from typing import TYPE_CHECKING, Generator

import pygame
import pygame.draw
import pygame.font
from itblib.globals.Colors import BLACK
from itblib.ui.animations.MultiSprite import MultiSprite

if TYPE_CHECKING:
    from itblib.Player import Player

class PlayerVersusAnimation(MultiSprite):
    def __init__(self, player1:"Player", player2:"Player", width, height):
        super().__init__([])
        self.font = pygame.font.SysFont('latinmodernmono', 60)
        self.p1 = player1
        self.p2 = player2
        self.width = width
        self.height = height
        self.pw = 200 #polygon width
        self.ph = 50 #polygon height
        self.p1x = 0
        self.p1y = 2
        self.p2x = self.width - self.pw
        self.p2y = height-self.ph-2
        self.polyanchors = [(0,0), (self.pw,0), (self.pw,self.ph), (30,self.ph)]
        self.s1 = pygame.Surface((self.pw, self.ph)).convert_alpha()
        self.s2 = pygame.Surface((self.pw, self.ph)).convert_alpha()
        self.s1.fill((0,0,0,0))
        self.s2.fill((0,0,0,0))
        pygame.draw.polygon(self.s1, self.p1.color, self.polyanchors)
        pygame.draw.polygon(self.s2, self.p2.color, self.polyanchors)
        p1name = self.font.render(self.p1.name, True, (255))
        p2name = self.font.render(self.p2.name, True, (255))
        self.s1.blit(p1name, (self.polyanchors[3][0]-5, self.polyanchors[0][1]+2))
        self.s2.blit(p2name, (self.polyanchors[3][0]-5, self.polyanchors[0][1]+2))
        self.clear_blit = pygame.Surface((self.width, self.ph+4))
        self.bar = pygame.Surface((self.width, self.ph+4))
        pygame.draw.line(self.bar, (100,100,100,255), (0,0), (self.width, 0), 2)
        pygame.draw.line(self.bar, (100,100,100,255), (0,self.ph+2), (self.width, self.ph+2), 2)
        self.clear_blit.fill(BLACK)
        self.retreating = False
        self.blits = []
        self._retreat_time = 2.0
        self._last_blit_time = 2.0

    def update(self, delta_time: float):
        self.animtime += delta_time
        self.p1x = self._posfunc()
        self.p2x = self.width/2 -self._posfunc()
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        self.blits.clear()
        self.blits.append((self.s1, pygame.Rect(self.p1x, self.p1y, self.pw, self.ph), pygame.Rect(0,0,self.pw, self.ph)))
        self.blits.append((self.s2, pygame.Rect(self.p2x, self.p2y, self.pw, self.ph), pygame.Rect(0,0,self.pw, self.ph)))
        if self.animtime >= self._retreat_time:
            r1, r2 = self._get_bar_rects(self._last_blit_time)
            self._last_blit_time = self.animtime
            yield from [
                (self.clear_blit, r1, self.bar.get_rect()), 
                (self.clear_blit, r2, self.bar.get_rect())
                ]
        r1, r2 = self._get_bar_rects(self.animtime)
        yield from [
            (self.bar, r1, self.bar.get_rect()),
            (self.bar, r2, self.bar.get_rect())
            ]
        yield from self.blits

    def _posfunc(self):
        return (((self.animtime-1)*7)**3)+((self.width-self.pw)/2)
    
    def _get_bar_rects(self, time:float) -> "tuple[pygame.Rect, pygame.Rect]":
        top_y = 0
        bot_y = self.height - self.ph - 4
        if time >= self._retreat_time:
            m = min(max(time-self._retreat_time,0)*2,1)
            top_y += m * -(self.ph+2)
            bot_y += m * (self.ph+2)
        size = (self.width, self.ph+4)
        top_rect = pygame.Rect((0, top_y), size)
        bot_rect = pygame.Rect((0, bot_y), size)
        return top_rect, bot_rect
