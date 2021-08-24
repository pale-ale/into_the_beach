from itblib.ui.TextureManager import Textures
from pygame.surface import Surface
from itblib.Vec import Vec
from itblib.SceneManager import SceneManager
from itblib.scenes.SceneBase import SceneBase
import pygame
import pygame.font
import pygame.transform
import itblib.gridelements.Units as Units

class RosterSelectionScene(SceneBase):
    """The user can select his lineup here."""
    def __init__(self, scenemanager:"SceneManager", width: int, height: int) -> None:
        super().__init__(scenemanager, width, height)
        self.titlefont = pygame.font.SysFont('latinmodernmono', 50)
        self.subfont = pygame.font.SysFont('latinmodernmono', 20)
        t = self.titlefont.render("Select your lineup here.", True, (50,200,150,255))
        esctext = self.subfont.render("ESC to quit, SPACE to queue", True, (50,200,150,255))
        self.image.blit(t, (width*.5 - t.get_width()*.5, 20))
        unitnames = ["BloodWraith",  "Saucer"]
        unitlist = Surface((width, 400)).convert_alpha()
        tilewidth = 128
        tilemarginx = 3
        tileheight = 128
        tilemarginy = 3
        tilecountline = 7 #int(width / (tilewidth + tilemarginx))
        freespace = width - tilecountline*tilewidth
        xspacer = freespace / (tilecountline+1)
        lines = 3
        for y in range(lines):
            for x in range(tilecountline):
                blitpos = (xspacer+x*(xspacer+tilewidth),  y*(tileheight+tilemarginy), tilewidth, tileheight)
                unitlist.fill(
                    (int(x/tilecountline*255), int(y/lines*255), 100, 255),
                    blitpos
                )
                unitindex = y*tilecountline+x
                if unitindex < len(unitnames):
                    tex = Textures.get_spritesheet("Unit"+unitnames[unitindex]+"SWIdle")[0]
                    s = Surface((tilewidth, tileheight)).convert_alpha()
                    pygame.transform.scale(tex, s.get_size(), s)
                    unitlist.blit(s, blitpos)
        self.image.blit(unitlist, (0, 100))

    def on_keyevent(self, keyevent):
        super().on_keyevent(keyevent)
        if keyevent.type == pygame.KEYDOWN:
            if keyevent.key == pygame.K_ESCAPE:
                self.scenemanager.load_scene("MainMenuScene")
            elif keyevent.key == pygame.K_SPACE:
                self.scenemanager.load_scene("GameScene")
    