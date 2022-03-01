from typing import Generator

import pygame
from itblib.globals.Colors import (GRAY_ACCENT_DARK, GRAY_ACCENT_LIGHT,
                                   IMAGE_BACKGROUND, WHITE)
from itblib.globals.Constants import HUD, STANDARD_TILE_SIZE
from itblib.gridelements.EffectsUI import EffectBaseUI
from itblib.gridelements.TilesUI import TileBaseUI
from itblib.input.Input import InputAcceptor
from itblib.ui.hud.EffectInfoGroup import EffectInfoGroup
from itblib.ui.widgets.TextBox import TextBox
from itblib.ui.widgets.Widget import Widget
from itblib.Vec import add


class TileDisplay(Widget, InputAcceptor):
    IMAGE_SIZE_BORDER = (2*HUD.IMAGE_BORDER_WIDTH + HUD.TILEDISPLAY.IMAGE_SIZE[0], 2*HUD.IMAGE_BORDER_WIDTH + HUD.TILEDISPLAY.IMAGE_SIZE[1])
    SIZE = (200,IMAGE_SIZE_BORDER[1])
    LABEL_SIZE = (SIZE[0] - IMAGE_SIZE_BORDER[0] - 2, HUD.LABEL_HEIGHT)
   
    def __init__(self):
        Widget.__init__(self)
        InputAcceptor.__init__(self)

        self._imagepos = (HUD.IMAGE_BORDER_WIDTH, HUD.IMAGE_BORDER_WIDTH)
        self._tilenamepos = (TileDisplay.IMAGE_SIZE_BORDER[0],HUD.IMAGE_BORDER_WIDTH)
        self._tiledescpos = None
        self._tileseffectpos = None

        self._tilenametextbox = TextBox(
            fontsize=32,
            bgcolor=GRAY_ACCENT_DARK, 
            linewidth=TileDisplay.LABEL_SIZE[0],
            lineheight=20
        )
        self._tiledesctextbox = TextBox(
            fontsize=15,
            bgcolor=GRAY_ACCENT_DARK, 
            linewidth=TileDisplay.LABEL_SIZE[0],
            lineheight=10
        )
        self._effectdisplay = EffectInfoGroup(TileDisplay.LABEL_SIZE[0])
        self._effectdisplay.parent = self
        self.register_input_listeners(self._effectdisplay)

        self._sub_blits:list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]] = []
        self.image = pygame.Surface((200,100)).convert_alpha()
        self._rect = self.image.get_rect()
        self.image.fill((0))
        self.tile:TileBaseUI = None
        self.effects:"list[EffectBaseUI]" = []
        self._draw_border()
    
    @property
    def tile(self):
        return self._tile

    @property
    def effects(self):
        return self._effects
    
    @tile.setter
    def tile(self, new_tile:TileBaseUI):
        """Set the new tile to display."""
        self.image.fill(GRAY_ACCENT_LIGHT)
        self._tile = new_tile
        self._tilenametextbox.text = new_tile.get_display_name() if new_tile else ""
        self._tiledesctextbox.text = new_tile.get_display_description() if new_tile else ""
        self._tiledescpos = add(self._tilenamepos, (0, self._tilenametextbox.image.get_height()+1))
        self._effectdisplay.position = add(self._tiledescpos, (0, self._tiledesctextbox.image.get_height()+3))
        self.update(0)
        self._draw_effect_separator()
    
    @effects.setter
    def effects(self, new_effects:"list[EffectBaseUI]"):
        """Set the new effects to display."""
        self._effects = new_effects
        self._effectdisplay.set_effects(new_effects)
        self.update(0)
        self._draw_effect_separator()
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from Widget.get_blits(self)
        yield from self._sub_blits
        yield from self._effectdisplay.get_blits()

    def update(self, dt):
        self.image.blit(self._tilenametextbox.image, self._tilenamepos)
        self.image.blit(self._tiledesctextbox.image, self._tiledescpos)
        self.image.fill(IMAGE_BACKGROUND, (*self._imagepos,*STANDARD_TILE_SIZE))
        self._sub_blits.clear()
        if self._tile:
            tile_rect = pygame.Rect(self._imagepos, STANDARD_TILE_SIZE) 
            self.image.blits([(blit[0], tile_rect , blit[2]) for blit in self._tile.get_blits()])
            for e in self._effects:
                self.image.blits([(blit[0], tile_rect, blit[2]) for blit in e.get_blits()])

    def _draw_border(self):
        pygame.draw.rect(
            self.image, 
            GRAY_ACCENT_DARK, 
            (
                0,0,
                TileDisplay.IMAGE_SIZE_BORDER[0] - HUD.IMAGE_BORDER_WIDTH/2,
                TileDisplay.IMAGE_SIZE_BORDER[1] - HUD.IMAGE_BORDER_WIDTH/2,
            ), 
            HUD.IMAGE_BORDER_WIDTH
            )

    def _draw_effect_separator(self):
        start = add(self._effectdisplay.position, (0,-2))
        end = add(start, (TileDisplay.LABEL_SIZE[0]-1,0))
        pygame.draw.line(self.image, WHITE, start, end)
