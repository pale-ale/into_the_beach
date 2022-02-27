import os

import pygame
import pygame.display
import pygame.sprite
import pygame.time

from itblib.gridelements.Effects import EffectFire, EffectMountain
from itblib.gridelements.EffectsUI import EffectFireUI, EffectMountainUI
from itblib.gridelements.Tiles import TileDirt
from itblib.gridelements.TilesUI import TileDirtUI
from itblib.ui.hud.TileDisplay import TileDisplay
from itblib.ui.IGraphics import IGraphics
from itblib.ui.TextureManager import Textures
from itblib.ui.widgets.KeyIcon import KeyIcon
from itblib.ui.widgets.TextBox import TextBox

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

test_tile_ui  = TileDirtUI(TileDirt(None, (0,0)))

test_effect_1 = EffectFireUI(EffectFire(None, (0,0)))
test_effect_2 = EffectMountainUI(EffectMountain(None, (0,0)))

tile_display.tile = test_tile_ui
tile_display.effects = [test_effect_1, test_effect_2]

scene_image = pygame.Surface(scene_size).convert_alpha()
preview_pos_index = 0

grid_count = 2
xpos = 0
gtime = 0.0

keyIcon = KeyIcon('R')
keyIcon.position = (100,100)
keyIcon2 = KeyIcon('R', pressed=True)
keyIcon2.position = (130,100)
textbox = TextBox(text = str(keyIcon.get_size()), pos = (100,130))

blittables:list[IGraphics] = [tile_display, keyIcon, keyIcon2, textbox]

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
        for b in blittables:
            scene_image.blits(b.get_blits())
        pygame.transform.scale(scene_image, screen.get_size(), screen)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
