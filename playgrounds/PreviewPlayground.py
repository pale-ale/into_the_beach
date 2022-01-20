import math
import os
from typing import Generator

import pygame
import pygame.display
import pygame.sprite
import pygame.time

from itblib.abilities.Abilities import RangedAttackAbility
from itblib.abilities.AbilityBase import AbilityBase
from itblib.abilities.previews.ConeAbilityPreview import ConeAttackAbilityPreview
from itblib.abilities.previews.RangedAttackAbilityPreview import \
    RangedAttackAbilityPreview
from itblib.Grid import Grid
from itblib.ui.GridUI import GridUI
from itblib.ui.TextureManager import Textures
from itblib.abilities.DreadfulNoiseAbility import DreadfulNoiseAbility

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

CONE_PREVIEW = ConeAttackAbilityPreview(RANGED_ABILITY)
CONE_PREVIEW._start = (2,2)
CONE_PREVIEW._color = (50,150,255)

PREVIEWS = [RANGED_PREVIEW, CONE_PREVIEW]
ABILITIES:list[AbilityBase] = [RANGED_ABILITY, CONE_ABILITY]
TARGETS = [
    MINIGRIDS[0].get_neighbors((2,2), ordinal=True, cardinal=True),
    MINIGRIDS[1].get_neighbors((2,2), ordinal=True, cardinal=True),
]

def update_targets():
    scene_image.fill(0)
    for i,a in enumerate(ABILITIES):
        a_targets = TARGETS[i]
        a.area_of_effect = {(a_targets[preview_pos_index % len(a_targets)], "Special")}
    CONE_PREVIEW.cone_center_angle += math.pi/8        

def main():
    global RUNNING
    global preview_pos_index
    gtime = 0.0
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
            gtime = 0
        for g in MINIGRIDUIS:
            scene_image.blits(g.get_blits())
            scene_image.blit(g.get_debug_surface(), g.pan)
        [g.update(dt) for g in MINIGRIDUIS]
        for i,p in enumerate(PREVIEWS):
            scene_image.blits(p.get_blit_func(MINIGRIDUIS[i].transform_grid_screen))
        pygame.transform.scale(scene_image, screen.get_size(), screen)
        pygame.display.update()
    pygame.quit()

def _vector_between(a,b,x) -> bool:
    """
    Calculate whether a vector is in between two other vectors.
    The "between" portion is chosen such that the angle between a nd b is minimal.
    Undefined for an angle of pi/2, i.e. when a and b are opposite to one another.
    @return: whether vector x is in between vectors a and b.
    """
    ax, ay = a
    bx, by = b
    xx, xy = x
    det_ax = ax*xx + ay*xy
    det_bx = bx*xx + by*xy
    return det_ax >= 0 and det_bx >= 0

def _get_circle(c, r) -> "Generator[tuple[int,int]]":
    """
    @c: circle center
    @r: radius
    @return: coordinates of tiles whose centers are within euclidean distance
    """
    left = c[0] - r
    right = c[0] + r
    top = c[1] - r
    bot = c[1] + r
    for y in range(top, bot+1):
        for x in range(left, right+1):
            if math.sqrt((c[0]-x)**2 + (c[1]-y)**2) <= r:
                yield (x,y)

if __name__ == '__main__':
    main()

