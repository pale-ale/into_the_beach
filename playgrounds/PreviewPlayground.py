import math
import os
import random
from typing import TYPE_CHECKING

import pygame
import pygame.display
import pygame.sprite
import pygame.time

from itblib.abilities.base_abilities.ability_base import AbilityBase
from itblib.abilities.base_abilities.ranged_abliity_base import \
    RangedAbilityBase
from itblib.abilities.dreadful_noise_ability import DreadfulNoiseAbility
from itblib.abilities.previews.abilitiy_preview_base import AbilityPreviewBase
from itblib.abilities.previews.cone_ability_preview import \
    ConeAttackAbilityPreview
from itblib.abilities.previews.ranged_ability_preview import \
    RangedAttackAbilityPreview
from itblib.abilities.previews.simple_ability_preview import SimpleAbilityPreview
from itblib.abilities.punch_ability import PunchAbility
from itblib.Grid import Grid
from itblib.ui.GridUI import GridUI
from itblib.ui.TextureManager import Textures

if TYPE_CHECKING:
    from typing import Type

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

PIXELSIZE = 2
RUNNING = True
FPS = 30
CLOCK = pygame.time.Clock()
UNIT_POS = (1,1)

pygame.display.init()
pygame.font.init()
info = pygame.display.Info()
screen_size = (info.current_w, info.current_h)
scene_size = (int(screen_size[0]/PIXELSIZE), int(screen_size[1]/PIXELSIZE))
screen = pygame.display.set_mode(screen_size)
Textures.load_textures()

scene_image = pygame.Surface(scene_size).convert_alpha()
preview_pos_index = 0

GRID_COUNT = 3
MINIGRIDS = [Grid(None, width=3, height=3) for x in range(GRID_COUNT)]
MINIGRIDUIS = [GridUI(MINIGRIDS[x]) for x in range(GRID_COUNT)]
ABILITY_CLASSES:"list[Type(AbilityBase)]" = [RangedAbilityBase, DreadfulNoiseAbility, PunchAbility]
ABILITIES:list[AbilityBase] = []
ABILITY_PREVIEW_CLASSES:"list[Type(AbilityPreviewBase)]" = [
    RangedAttackAbilityPreview,
    ConeAttackAbilityPreview,
    SimpleAbilityPreview
]
PREVIEWS:list[AbilityPreviewBase] = []
global_time = 0.0

TARGETS = [
    list(MINIGRIDS[0].get_neighbors(UNIT_POS, ordinal=True, cardinal=True)),
    list(MINIGRIDS[1].get_neighbors(UNIT_POS, ordinal=True, cardinal=True)),
    list(MINIGRIDS[2].get_neighbors(UNIT_POS, ordinal=True))
]

def setup_minigrids():
    """..."""
    for i,mg in enumerate(MINIGRIDS):
        mgui = MINIGRIDUIS[i]
        mg.update_observer(mgui)
        unit = mg.add_unit(UNIT_POS, 2, 0)
        ability = unit.ability_component.add_ability(ABILITY_CLASSES[i])
        ability.primed = True
        ABILITIES.append(ability)
        PREVIEWS.append(ABILITY_PREVIEW_CLASSES[i](ability))
        mgui.update_pan((mgui.width*i, 0))


def update_targets():
    """Choose new targets"""
    scene_image.fill(0)
    for i,grid in enumerate(MINIGRIDS):
        ability = ABILITIES[i]
        ability_targets = TARGETS[i]
        ability.area_of_effect = {(random.choice(ability_targets), "Special")}
    ABILITIES[1].cone_direction -= math.pi/4
    ABILITIES[1].cone_spread_angle = math.pi/4
    ABILITIES[1].cone_len_tiles = 1
    ABILITIES[1].on_select_ability()
    ABILITIES[2].on_select_ability()

def main():
    """..."""
    global RUNNING
    global preview_pos_index
    global global_time
    setup_minigrids()
    update_targets()
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                RUNNING = False
        dt = CLOCK.tick(FPS)/1000.0
        global_time += dt
        if global_time >= 1:
            preview_pos_index += 1
            update_targets()
            global_time = 0.0
        for g in MINIGRIDUIS:
            scene_image.blits(g.get_blits())
            scene_image.blit(g.get_debug_surface(), g._pan)
        [g.update(dt) for g in MINIGRIDUIS]
        for i,p in enumerate(PREVIEWS):
            scene_image.blits(p.get_blit_func(MINIGRIDUIS[i].transform_grid_screen))
        pygame.transform.scale(scene_image, screen.get_size(), screen)
        pygame.display.update()
    pygame.quit()



if __name__ == '__main__':
    main()

