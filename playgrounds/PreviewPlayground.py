import math
import os
from typing import Type

import pygame
import pygame.display
import pygame.sprite
import pygame.time

from itblib.abilities.baseAbilities.AbilityBase import AbilityBase
from itblib.abilities.baseAbilities.RangedAttackAbilityBase import \
    RangedAttackAbility
from itblib.abilities.DreadfulNoiseAbility import DreadfulNoiseAbility
from itblib.abilities.previews.AbilityPreviewBase import AbilityPreviewBase
from itblib.abilities.previews.ConeAbilityPreview import \
    ConeAttackAbilityPreview
from itblib.abilities.previews.RangedAttackAbilityPreview import \
    RangedAttackAbilityPreview
from itblib.abilities.previews.SimpleAbilityPreview import SimpleAbilityPreview
from itblib.abilities.PunchAbility import PunchAbility
from itblib.Grid import Grid
from itblib.ui.GridUI import GridUI
from itblib.ui.TextureManager import Textures

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

PIXELSIZE = 2
RUNNING = True
FPS = 30
CLOCK = pygame.time.Clock()
UNIT_POS = (1,1)

pygame.display.init()
pygame.font.init()
i = pygame.display.Info()
screen_size = (i.current_w, i.current_h)
scene_size = (int(screen_size[0]/PIXELSIZE), int(screen_size[1]/PIXELSIZE))
screen = pygame.display.set_mode(screen_size)
Textures.load_textures()

scene_image = pygame.Surface(scene_size).convert_alpha()
preview_pos_index = 0

grid_count = 3
MINIGRIDS = [Grid(None, width=3, height=3) for x in range(grid_count)]
MINIGRIDUIS = [GridUI(MINIGRIDS[x]) for x in range(grid_count)]
ABILITY_CLASSES:"list[Type(AbilityBase)]" = [RangedAttackAbility, DreadfulNoiseAbility, PunchAbility]
ABILITIES:list[AbilityBase] = []
ABILITY_PREVIEW_CLASSES:"list[Type(AbilityPreviewBase)]" = [RangedAttackAbilityPreview, ConeAttackAbilityPreview, SimpleAbilityPreview]
PREVIEWS:list[AbilityPreviewBase] = []
gtime = 0.0
for i,mg in enumerate(MINIGRIDS):
    mgui = MINIGRIDUIS[i]
    mg.update_observer(mgui)
    unit = mg.add_unit(UNIT_POS, 2, 0)
    ability = unit.ability_component.add_ability(ABILITY_CLASSES[i])
    ability.primed = True
    ABILITIES.append(ability)
    PREVIEWS.append(ABILITY_PREVIEW_CLASSES[i](ability))
    mgui.update_pan((mgui.width*i, 0))

TARGETS = [
    MINIGRIDS[0].get_neighbors(UNIT_POS, ordinal=True, cardinal=True),
    MINIGRIDS[1].get_neighbors(UNIT_POS, ordinal=True, cardinal=True),
    MINIGRIDS[2].get_neighbors(UNIT_POS, ordinal=True)
]

def update_targets():
    global gtime
    scene_image.fill(0)
    for i,grid in enumerate(MINIGRIDS):
        unit = grid.get_unit(UNIT_POS)
        ability = ABILITIES[i]
        ability_targets = TARGETS[i]
        ability.area_of_effect = {(ability_targets[preview_pos_index % len(ability_targets)], "Special")}
    ABILITIES[1].cone_direction -= math.pi/4
    ABILITIES[1].cone_spread_angle = math.pi/4
    ABILITIES[1].cone_len_tiles = 1
    ABILITIES[1].on_select_ability()
    ABILITIES[2].on_select_ability()

def main():
    global RUNNING
    global preview_pos_index
    global gtime
    update_targets()
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                RUNNING = False
        dt = CLOCK.tick(FPS)/1000.0
        gtime += dt
        if gtime >= .3:
            preview_pos_index += 1
            update_targets()
            gtime = 0.0
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

