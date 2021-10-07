from typing import TYPE_CHECKING
import pygame
import pygame.draw
import pygame.font
from itblib.ui.animations.MultiSprite import MultiSprite
if TYPE_CHECKING:
    from itblib.Player import Player

class PlayerVersusAnimation(MultiSprite):
    def __init__(self, player1:"Player", player2:"Player", width, height):
        super().__init__([], width=width, height=height)
        self.font = pygame.font.SysFont('latinmodernmono', 60)
        self.p1 = player1
        self.p2 = player2
        self.width = width
        self.pw = 450 #polygon width
        self.ph = 100 #polygon height
        self.p1polyanchors = [(0,10), (self.pw,10), (self.pw,self.ph), (30,self.ph)]
        self.p2polyanchors = [ (x,height-y) for x,y in self.p1polyanchors]

    def update(self, dt: float):
        self.image.fill(0)
        self.animtime += dt
        p1polypoints = [(x+(self.width-self.pw)/2 + self._posfunc(self.animtime), y) for x,y in self.p1polyanchors]
        p2polypoints = [(x+(self.width-self.pw)/2 - self._posfunc(self.animtime), y) for x,y in self.p2polyanchors]
        pygame.draw.polygon(self.image, self.p1.color, p1polypoints)
        pygame.draw.polygon(self.image, self.p2.color, p2polypoints)
        p1name = self.font.render(self.p1.name, True, (255))
        p2name = self.font.render(self.p2.name, True, (255))
        self.image.blit(p1name, (p1polypoints[3][0], p1polypoints[0][1]))
        self.image.blit(p2name, (p2polypoints[3][0], p2polypoints[2][1]))

    def _posfunc(self, animtime:float):
        return (((animtime-1)*7)**3)+((self.width-self.pw)/2.3)
