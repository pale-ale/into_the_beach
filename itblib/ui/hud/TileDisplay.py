from typing import Generator

import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.globals.Colors import (GRAY_ACCENT_DARK, GRAY_ACCENT_LIGHT,
                                   IMAGE_BACKGROUND, WHITE)
from itblib.globals.Constants import HUD, STANDARD_TILE_SIZE
from itblib.gridelements.EffectsUI import EffectBaseUI
from itblib.gridelements.TilesUI import TileBaseUI
from itblib.input.Input import InputAcceptor
from itblib.ui.hud.EffectInfoGroup import EffectInfoGroup
from itblib.ui.PerfSprite import PerfSprite
from itblib.ui.TextBox import TextBox
from itblib.Vec import add


class TileDisplay(ComponentAcceptor, InputAcceptor, PerfSprite):
    IMAGE_SIZE = STANDARD_TILE_SIZE
    IMAGE_SIZE_BORDER = (2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[0], 2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[1])
    SIZE = (200,IMAGE_SIZE_BORDER[1])
    LABEL_SIZE = (SIZE[0] - IMAGE_SIZE_BORDER[0] - 2, HUD.LABEL_HEIGHT)
   
    def __init__(self):
        ComponentAcceptor.__init__(self)
        InputAcceptor.__init__(self)
        PerfSprite.__init__(self)
        self.tfc = TransformComponent()
        self.tfc.attach_component(self)

        self.imagepos = (HUD.IMAGE_BORDER_WIDTH, HUD.IMAGE_BORDER_WIDTH)
        self.tilenamepos = (TileDisplay.IMAGE_SIZE_BORDER[0],HUD.IMAGE_BORDER_WIDTH)
        self.tiledescpos = None
        self.tileseffectpos = None

        self.tilenametextbox = TextBox(
            fontsize=32,
            bgcolor=GRAY_ACCENT_DARK, 
            linewidth=TileDisplay.LABEL_SIZE[0],
            lineheight=20
        )
        self.tiledesctextbox = TextBox(
            fontsize=15,
            bgcolor=GRAY_ACCENT_DARK, 
            linewidth=TileDisplay.LABEL_SIZE[0],
            lineheight=10
        )
        self.effectdisplay = EffectInfoGroup(TileDisplay.LABEL_SIZE[0])
        self.effectdisplay.tfc.set_transform_target(self)
        self.register_input_listeners(self.effectdisplay)

        self.sub_blits:list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]] = []
        self.image = pygame.Surface((200,100)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0))
        self.displaytile:TileBaseUI = None
        self.set_displaytile_effects(None, [])
        self.draw_border()

    def draw_border(self):
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
    
    def draw_effect_separator(self):
        start = add(self.effectdisplay.tfc.get_position(), (0,-2))
        end = add(start, (TileDisplay.LABEL_SIZE[0],0))
        pygame.draw.line(self.image, WHITE, start, end)

    def set_displaytile_effects(self, tile:TileBaseUI, effects:"list[EffectBaseUI]"):
        """Set the new tile and effects to display."""
        self.image.fill(GRAY_ACCENT_LIGHT)
        self.displaytile = tile
        self.tilenametextbox.text = tile.get_display_name() if tile else ""
        self.tilenametextbox.update_textbox()
        self.tiledesctextbox.text = tile.get_display_description() if tile else ""
        self.tiledesctextbox.update_textbox()
        self.tiledescpos = add(self.tilenamepos, (0, self.tilenametextbox.image.get_height()+1))
        self.effectdisplay.tfc.relative_position = add(self.tiledescpos, (0, self.tiledesctextbox.image.get_height()+3))
        self.effectdisplay.set_effects(effects)
        self.update(0)
    
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.image, self.rect, self.image.get_rect())
        yield from self.sub_blits
        yield from self.effectdisplay.get_blits()

    def update(self, dt):
        self.image.blit(self.tilenametextbox.image, self.tilenamepos)
        self.image.blit(self.tiledesctextbox.image, self.tiledescpos)
        self.image.fill(IMAGE_BACKGROUND, (*self.imagepos,*STANDARD_TILE_SIZE))
        self.sub_blits.clear()
        if self.displaytile:
            self.image.blits([(blit[0], pygame.Rect(*self.imagepos, *STANDARD_TILE_SIZE) , blit[2]) for blit in self.displaytile.get_blits()])
        self.draw_effect_separator()
