from typing import Generator

import pygame
from itblib.gridelements.Effects import EffectBase
from itblib.ui.PerfSprite import PerfSprite
from itblib.ui.TextBox import TextBox


class EffectInfoElement(PerfSprite):
    def __init__(self, effect: EffectBase) -> None:
        super().__init__()
        self.title_tb = TextBox(effect.get_display_name(), fontsize=13, bgcolor=(50,50,50), lineheight=16)
        self.desc_tb = TextBox(effect.get_display_description(), fontsize=8, pos=(0,17), bgcolor=(50,50,50), linewidth=132, lineheight=10)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.title_tb.image, self.title_tb.rect, self.title_tb.image.get_rect())
        yield (self.desc_tb.image , self.desc_tb.rect , self.desc_tb.image.get_rect())
