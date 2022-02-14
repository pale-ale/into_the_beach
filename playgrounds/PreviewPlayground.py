import math
import os

import pygame
import pygame.display
import pygame.sprite
import pygame.time

from itblib.abilities.baseAbilities.AbilityBase import AbilityBase
from itblib.abilities.baseAbilities.RangedAttackAbilityBase import \
    RangedAttackAbility
from itblib.abilities.DreadfulNoiseAbility import DreadfulNoiseAbility
from itblib.abilities.previews.ConeAbilityPreview import \
    ConeAttackAbilityPreview
from itblib.abilities.previews.RangedAttackAbilityPreview import \
    RangedAttackAbilityPreview
from itblib.Grid import Grid
from itblib.ui.GridUI import GridUI
from itblib.ui.TextureManager import Textures

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

PIXELSIZE = 2
RUNNING = True
FPS = 30
CLOCK = pygame.time.Clock()

pygame.display.init()
pygame.font.init()
i = pygame.display.Info()
screen_size = (i.current_w, i.current_h)
scene_size = (int(screen_size[0]/PIXELSIZE), int(screen_size[1]/PIXELSIZE))
screen = pygame.display.set_mode(screen_size)
Textures.load_textures()

scene_image = pygame.Surface(scene_size).convert_alpha()
preview_pos_index = 0

grid_count = 2
MINIGRIDS = [Grid(None, width=5, height=5) for x in range(grid_count)]
MINIGRIDUIS = [GridUI(MINIGRIDS[x]) for x in range(grid_count)]
xpos = 0
gtime = 0.0
for i,mg in enumerate(MINIGRIDS):
    mgui = MINIGRIDUIS[i]
    mg.update_observer(mgui)
    mg.add_unit((2,2), 2, 0)
    mgui.update_pan((xpos, 0))
    xpos += mgui.width

RANGED_ABILITY = RangedAttackAbility(None)
RANGED_ABILITY.primed = True

CONE_ABILITY = DreadfulNoiseAbility(None)
CONE_ABILITY.primed = True

RANGED_PREVIEW = RangedAttackAbilityPreview(RANGED_ABILITY)
RANGED_PREVIEW._start = (2,2)
RANGED_PREVIEW._color = (50,255,100)

CONE_PREVIEW = ConeAttackAbilityPreview(CONE_ABILITY)
CONE_PREVIEW._start = (2,2)
CONE_PREVIEW._color = (50,150,255)

PREVIEWS = [RANGED_PREVIEW, CONE_PREVIEW]
ABILITIES:list[AbilityBase] = [RANGED_ABILITY, CONE_ABILITY]
TARGETS = [
    MINIGRIDS[0].get_neighbors((2,2), ordinal=True, cardinal=True),
    MINIGRIDS[1].get_neighbors((2,2), ordinal=True, cardinal=True),
]

def update_targets():
    global gtime
    scene_image.fill(0)
    for i,a in enumerate(ABILITIES):
        a_targets = TARGETS[i]
        a.area_of_effect = {(a_targets[preview_pos_index % len(a_targets)], "Special")}
    CONE_ABILITY.cone_direction -= math.pi/4
    CONE_ABILITY.cone_spread_angle = math.pi/4
    CONE_ABILITY.cone_len_tiles = 3
    CONE_ABILITY.on_select_ability()

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

