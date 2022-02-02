from typing import Generator

import pygame
from itblib.globals.Constants import HUD, STANDARD_TILE_SIZE
from itblib.gridelements.EffectsUI import EffectBaseUI
from itblib.gridelements.TilesUI import TileBaseUI
from itblib.ui.PerfSprite import PerfSprite
from itblib.ui.TextBox import TextBox
from itblib.Vec import add
from itblib.ui.hud.EffectInfoElement import EffectInfoElement

class TileDisplay(PerfSprite):
    IMAGE_SIZE = STANDARD_TILE_SIZE
    IMAGE_SIZE_BORDER = (2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[0], 2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[1])
    SIZE = (200,IMAGE_SIZE_BORDER[1])
    LABEL_SIZE = (SIZE[0] - IMAGE_SIZE_BORDER[0], HUD.LABEL_HEIGHT)
   
    def __init__(self):
        super().__init__()
        self.imagepos = (HUD.IMAGE_BORDER_WIDTH, HUD.IMAGE_BORDER_WIDTH)
        self.titlepos = (TileDisplay.IMAGE_SIZE_BORDER[0],HUD.IMAGE_BORDER_WIDTH)
        self.defaultimagecolor = (30,0,0,255)
        self.defaulttextboxcolor = (50,50,50,255)
        self.tilenametextbox = TextBox(bgcolor=self.defaulttextboxcolor, lineheight=22)
        self.font = pygame.font.SysFont('latinmodernmono', HUD.FONT_SIZE)
        self.image = pygame.Surface((200,100)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0))
        self.displaytile:TileBaseUI = None
        self.displayeffects:"list[EffectBaseUI]" = None
        self.set_displaytile_effects(None, None)
        self.draw_border()

    def draw_border(self):
        pygame.draw.rect(
            self.image, 
            HUD.IMAGE_BORDER_COLOR, 
            (
                0,0,
                TileDisplay.IMAGE_SIZE_BORDER[0] - HUD.IMAGE_BORDER_WIDTH/2,
                TileDisplay.IMAGE_SIZE_BORDER[1] - HUD.IMAGE_BORDER_WIDTH/2,
            ), 
            HUD.IMAGE_BORDER_WIDTH
            )

    def set_displaytile_effects(self, tile:TileBaseUI, effects:"list[EffectBaseUI]"):
        """Set the new tile and effects to display."""
        self.image.fill((100,100,100,255))
        self.displaytile = tile
        self.tilenametextbox.text = tile.get_display_name() if tile else ""
        self.tilenametextbox.update_textbox()
        self.displayeffects = effects
        self.update(0)
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.image, self.rect, self.image.get_rect())
        
    def update(self, dt):
        self.image.blit(self.tilenametextbox.image, self.titlepos)
        self.image.fill(self.defaultimagecolor, (*self.imagepos,*STANDARD_TILE_SIZE))
        if self.displaytile:
            self.image.blits([(blit[0], pygame.Rect(*self.imagepos, *STANDARD_TILE_SIZE) , blit[2]) for blit in self.displaytile.get_blits()])
        if self.displayeffects:
            for i,e in enumerate(self.displayeffects):
                edisplay = EffectInfoElement(e._parentelement)
                self.image.blits([(blit[0], pygame.Rect(*self.imagepos, *STANDARD_TILE_SIZE) , blit[2]) for blit in e.get_blits()])
                for s,g,l in edisplay.get_blits():
                    self.image.blits([(s, pygame.Rect(*add((self.titlepos[0], 25*(i+1)), g), *STANDARD_TILE_SIZE) , l)])

