from typing import Generator

import pygame
from itblib.gridelements.Effects import EffectBase
from itblib.ui.PerfSprite import PerfSprite
from itblib.ui.TextBox import TextBox


class EffectInfoElement(PerfSprite):
    def __init__(self, effect: EffectBase, width: int) -> None:
        super().__init__()
        self.title_tb = TextBox(effect.get_display_name(),        fontsize=16, bgcolor=(50,50,50), linewidth=width)
        self.desc_tb =  TextBox(effect.get_display_description(), fontsize=16, bgcolor=(50,50,50), linewidth=width-5, pos=(5,14))

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.title_tb.image, self.title_tb.rect, self.title_tb.image.get_rect())
        yield (self.desc_tb.image , self.desc_tb.rect , self.desc_tb.image.get_rect())
