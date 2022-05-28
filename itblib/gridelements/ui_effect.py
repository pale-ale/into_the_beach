"""
A Collection of EffectUIs, used as a screen representation of WorldEffects and StatusEffects.
"""

import math
import random
from typing import TYPE_CHECKING

import pygame
from itblib.components import TransformComponent
from itblib.globals.Colors import TEXTURE_MISSING
from itblib.globals.Enums import RIVER
from itblib.gridelements.GridElementUI import GridElementUI
from itblib.gridelements.world_effects import WorldEffectBase
from itblib.ui.IDisplayable import IDisplayable
from itblib.ui.particles import FireParticleSpawner
from itblib.ui.TextureManager import Textures

if TYPE_CHECKING:
    from typing import Generator


class EffectBaseUI(GridElementUI, IDisplayable):
    """Base class of the UI Effects, displaying World/StatusEffects."""
    def __init__(self, effect:WorldEffectBase, framespeed:float=.2, autoplay=True):
        super().__init__(parentelement=effect, direction=None, framespeed=framespeed)
        if autoplay:
            self.looping = False
            self.start()

    def get_display_description(self) -> str:
        return self._parentelement.get_display_description()

    def get_display_name(self) -> str:
        return self._parentelement.get_display_name()

    def get_icon(self) -> pygame.Surface:
        icon = pygame.Surface((16,16))
        icon.fill(TEXTURE_MISSING)
        return icon


class EffectRiverUI(EffectBaseUI):
    """Displays a river. Uses proximity texturing to connect to neighbours."""
    def _update(self, delta_time:float):
        """Updates neighbors every tick."""
        grid = self._parentelement.grid
        pos = self._parentelement.position
        neighborposs = grid.get_neighbors(pos)
        riverposs = []
        for test_pos in neighborposs:
            for effect in grid.get_worldeffects(test_pos):
                if type(effect).__name__ == "EffectRiver":
                    riverposs.append(test_pos)
        if len(riverposs) == 0:
            imageid = 4
        elif len(riverposs) == 1:
            imageid = 5
        elif len(riverposs) == 2:
            prev, next = riverposs
            prevdelta = (pos[0] - prev[0], pos[1] - prev[1])
            nextdelta = (next[0] - pos[0], next[1] - pos[1])
            imageid = RIVER[(*nextdelta, *prevdelta)]
        else:
            print("EffectRiverUI: Weird riverposs:", riverposs)
            return
        self.framenumber = imageid


class EffectFireUI(EffectBaseUI):
    """Displays fire."""
    def __init__(self, effect: WorldEffectBase, framespeed: float = 0.5):
        super().__init__(effect, framespeed=framespeed, autoplay=False)
        self._fire_particles = FireParticleSpawner()
        self._fire_particles.get_component(TransformComponent).set_transform_target(self)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self._fire_particles.get_blits()

    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Ablaze")[0]

    def _update(self, delta_time: float):
        """Update the fire particles."""
        self._fire_particles.update(delta_time)

class EffectMountainUI(EffectBaseUI):
    """Displays a mountain."""
    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Mountain")[0]


class EffectWheatUI(EffectBaseUI):
    """Displays a wheat field."""
    def get_icon(self) -> pygame.Surface:
        return Textures.get_spritesheet("Wheat")[0]

class EffectHealUI(EffectBaseUI):
    """Displays a heal."""
    def __init__(self, effect: WorldEffectBase, framespeed: float = 0.1, autoplay=True):
        super().__init__(effect, framespeed, autoplay)

class EffectStartingAreaUI(EffectBaseUI):
    """Displays the player's starting area."""
    def __init__(self, effect: WorldEffectBase, framespeed: float = 0.2, autoplay=False):
        super().__init__(effect, framespeed, autoplay)

    def get_display_name(self) -> str:
        return "Drop Zone"
