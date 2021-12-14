from typing import Generator

import pygame
from itblib.globals.Constants import HUD, STANDARD_TILE_SIZE
from itblib.gridelements.EffectsUI import EffectBaseUI
from itblib.gridelements.TilesUI import TileBaseUI
from itblib.ui.PerfSprite import PerfSprite
from itblib.Vec import add


class TileDisplay(PerfSprite):
    IMAGE_SIZE = STANDARD_TILE_SIZE
    IMAGE_SIZE_BORDER = (2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[0], 2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[1])
    SIZE = (200,IMAGE_SIZE_BORDER[1])
    LABEL_SIZE = (SIZE[0] - IMAGE_SIZE_BORDER[0], HUD.LABEL_HEIGHT)
   
    def __init__(self):
        super().__init__()
        self.imagepos = (HUD.IMAGE_BORDER_WIDTH, HUD.IMAGE_BORDER_WIDTH)
        self.titlepos = (TileDisplay.IMAGE_SIZE_BORDER[0],0)
        self.defaultimagecolor = (30,0,0,255)
        self.defaulttextboxcolor = (50,50,50,255)
        self.font = pygame.font.SysFont('latinmodernmono', HUD.FONT_SIZE)
        self.image = pygame.Surface((200,200)).convert_alpha()
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
        self.displaytile = tile
        self.displayeffects = effects
        self.update(0)
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.image, self.rect, self.image.get_rect())
        
    def update(self, dt):
        self.image.fill(self.defaultimagecolor, (*self.imagepos,*STANDARD_TILE_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.titlepos,128,20))
        if self.displaytile:
            title_text = self.font.render(self.displaytile.get_display_name(), True, (255,255,255,255))
            self.image.blit(
                title_text, 
                add(self.titlepos, (0, (self.LABEL_SIZE[1]-title_text.get_height())/2))
            )
            self.image.blits([(blit[0], pygame.Rect(*self.imagepos, *STANDARD_TILE_SIZE) , blit[2]) for blit in self.displaytile.get_blits()])
        if self.displayeffects:
            for e in self.displayeffects:
                self.image.blits([(blit[0], pygame.Rect(*self.imagepos, *STANDARD_TILE_SIZE) , blit[2]) for blit in e.get_blits()])
