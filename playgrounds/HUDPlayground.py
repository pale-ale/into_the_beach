import sys
import os
sys.path.append(os.path.expanduser('~/into_the_beach'))


import pygame
import pygame.display
import pygame.sprite
import pygame.time
from itblib.gridelements.Tiles import TileDirt, TileLava
from itblib.gridelements.TilesUI import TileDirtUI, TileLavaUI
from itblib.gridelements.ui_effect import EffectFireUI, EffectMountainUI
from itblib.gridelements.world_effects import EffectFire, EffectMountain
from itblib.ui.animations.projectile import ProjectileAnimation
from itblib.ui.hud.hud import TileDisplay
from itblib.ui.IGraphics import IGraphics
from itblib.ui.TextureManager import Textures
from itblib.ui.widgets.ui_widget import KeyIcon, TextBox

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

# test_tile_ui  = TileDirtUI(TileDirt(None, (0,0)))
test_tile_ui  = TileLavaUI(TileLava(None, (0,0)))
test_tile_ui.frametime = 0.15

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
keyIcon.position = (100,120)
keyIcon2 = KeyIcon('ESC', fontsize=16)
keyIcon2.position = (130,120)
keyIcon3 = KeyIcon('\u2423', fontsize=32)
keyIcon3.position = (160,120)
textbox = TextBox(text = str(keyIcon.get_size()))
textbox.parent = keyIcon
textbox.position = (0,35)

textbox2 = TextBox(text = str(textbox.get_size()))
textbox2.parent = textbox
textbox2.position = (0, 12)

posfunc1 = lambda x: (75*x, 200)
posfunc2 = lambda x: (300, 300)
projectile = ProjectileAnimation(5.0, posfunc1)

blittables:list[IGraphics] = [tile_display, keyIcon, keyIcon2, keyIcon3, textbox, textbox2, projectile]

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
        test_tile_ui.update(dt)
        test_effect_1.update(dt)
        scene_image.fill((0), ( (projectile._pos[0]-25, projectile._pos[1]-25), (50,50)))
        projectile.update(dt)
        for b in blittables:
            scene_image.blits(b.get_blits())
        scene_image.blits(test_effect_1.get_blits())
        scene_image.blits(projectile._particles_spawner.get_blits())
        pygame.transform.scale(scene_image, screen.get_size(), screen)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
