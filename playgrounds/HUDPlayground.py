import math
import os

import pygame
import pygame.display
import pygame.sprite
import pygame.time
from itblib.gridelements.Effects import EffectFire
from itblib.gridelements.EffectsUI import EffectFireUI
from itblib.gridelements.Tiles import TileDirt
from itblib.gridelements.TilesUI import TileDirtUI

from itblib.ui.hud.TileDisplay import TileDisplay
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

tile_display = TileDisplay()

test_tile_ui = TileDirtUI(TileDirt(None, (0,0)))
test_effect_1 = EffectFireUI(EffectFire(None, (0,0)))

tile_display.set_displaytile_effects(test_tile_ui, [test_effect_1])

scene_image = pygame.Surface(scene_size).convert_alpha()
preview_pos_index = 0

grid_count = 2
xpos = 0
gtime = 0.0

def main():
    global RUNNING
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                RUNNING = False
        dt = CLOCK.tick(FPS)/1000.0
        scene_image.blits(tile_display.get_blits())
        pygame.transform.scale(scene_image, screen.get_size(), screen)
        pygame.display.update()
    pygame.quit()



if __name__ == '__main__':
    main()

