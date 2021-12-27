import math
import os
from typing import Generator

import pygame
import pygame.display
import pygame.sprite
import pygame.time

from itblib.abilities.Abilities import RangedAttackAbility
from itblib.abilities.previews.RangedAttackAbilityPreview import \
    RangedAttackAbilityPreview
from itblib.Grid import Grid
from itblib.Log import log
from itblib.Maps import MapGrasslands
from itblib.ui.GridUI import GridUI
from itblib.ui.TextureManager import Textures

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

PIXELSIZE = 2
RUNNING = True
FPS = 30
CLOCK = pygame.time.Clock()

pygame.display.init()
i = pygame.display.Info()
screen_size = (i.current_w, i.current_h)
scene_size = (int(screen_size[0]/PIXELSIZE), int(screen_size[1]/PIXELSIZE))
screen = pygame.display.set_mode(screen_size)
Textures.load_textures()

scene_image = pygame.Surface(scene_size).convert_alpha()
preview_pos_index = 0

TRANSFORM_FUNC = lambda pos: ((pos[0]-pos[1])*16, pos[1]*64)

RANGED_ABILITY = RangedAttackAbility(None)
RANGED_ABILITY.primed = True

RANGED_PREVIEW = RangedAttackAbilityPreview(RANGED_ABILITY)
RANGED_PREVIEW._start = (1,3)
RANGED_PREVIEW._color = (50,255,100)

PREVIEWS = [RANGED_PREVIEW]
ABILITIES = [RANGED_ABILITY]
TARGETS = [
    [(0,2), (0,3), (0,4), (1,4), (2,4), (2,3), (2,2), (1,2)]
]

MINIGRID = Grid(None, width=10, height=10)
MINIGRIDUI = GridUI(MINIGRID)
#MINIGRIDUI.update_pan((0,0))
MINIGRID.update_observer(MINIGRIDUI)

MINIGRID.load_map(MapGrasslands(), True)
MINIGRID.add_unit((0,0), 2, 0)

def update_targets():
    #scene_image.fill(0)
    for i,a in enumerate(ABILITIES):
        a_targets = TARGETS[i]
        a.area_of_effect = {(a_targets[preview_pos_index % len(a_targets)], "Special")}

def transform_grid_world(gridpos:"tuple[int,int]"):
    return (
        int( (gridpos[1]-gridpos[0]) * 32),
        int( (gridpos[1]+gridpos[0]) * 22)
    )

def main():
    global RUNNING
    global preview_pos_index
    gtime = 0.0
    log("Starting ..", 0)
    log("Started ", 0)
    update_targets()
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                RUNNING = False
        dt = CLOCK.tick(FPS)/1000.0
        gtime += dt
        if gtime >= 1:
            preview_pos_index += 1
            update_targets()
            gtime = 0
        scene_image.blits(MINIGRIDUI.get_blits())
        scene_image.blit(MINIGRIDUI.get_debug_surface(), MINIGRIDUI.pan)
        MINIGRIDUI.update(dt)
        for p in PREVIEWS:
            scene_image.blits(p.get_blit_func(transform_grid_world))
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

