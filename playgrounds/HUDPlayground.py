import os
import sys

from itblib.Vec import IVector2

sys.path.append(os.path.expanduser('~/into_the_beach'))

import pygame
import pygame.display
import pygame.sprite
import pygame.time

from itblib.gridelements.Tiles import TileLava
from itblib.gridelements.TilesUI import TileLavaUI
from itblib.gridelements.units.units import UnitKnight
from itblib.gridelements.UnitsUI import UnitKnightUI
from itblib.gridelements.ui_effect import EffectFireUI, EffectMountainUI
from itblib.gridelements.world_effects import EffectFire, EffectMountain
from itblib.ui.hud.hud import TileDisplay, UnitDisplay
from itblib.ui.TextureManager import Textures

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

from math import sin

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

tile_display = TileDisplay()
unit_display = UnitDisplay()

test_tile_ui = TileLavaUI(TileLava(None, IVector2(0,0)))
test_tile_ui._frametime = 0.15
test_unit_ui = UnitKnightUI(UnitKnight(None, IVector2(0,0), 0))
test_unit_ui._frametime = 0.15

test_effect_1 = EffectFireUI(EffectFire(None, IVector2(0,0)))
test_effect_2 = EffectMountainUI(EffectMountain(None, IVector2(0,0)))

tile_display.tile = test_tile_ui
tile_display.effects = [test_effect_1, test_effect_2]

unit_display.displayunit = test_unit_ui._parentelement
unit_display.set_displayunit(test_unit_ui)
unit_display.rect.left = scene_size[0] - unit_display.rect.width

scene_image = pygame.Surface(scene_size).convert_alpha()
preview_pos_index = 0

grid_count = 2
xpos = 0
gtime = 0.0

def main():
    global RUNNING, gtime
    while RUNNING:
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    RUNNING = False
                else:
                    tile_display.handle_key_event(event)
        dt = CLOCK.tick(FPS)/1000.0
        gtime += dt
        test_tile_ui.tick(dt)
        test_effect_1.tick(dt)
        test_unit_ui.tick(dt)
        scene_image.blits(tile_display.get_blits())
        scene_image.blits(unit_display.get_blits())
        scene_image.blits(test_effect_1.get_blits())
        pygame.transform.scale(scene_image, screen.get_size(), screen)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
