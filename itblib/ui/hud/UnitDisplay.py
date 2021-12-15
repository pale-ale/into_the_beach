from typing import Generator

import pygame
from itblib.components.TransformComponent import TransformComponent
from itblib.globals.Colors import BLACK, PHASECOLORS
from itblib.globals.Constants import HUD, STANDARD_UNIT_SIZE
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.gridelements.UnitsUI import UnitBaseUI
from itblib.ui.PerfSprite import PerfSprite
from itblib.ui.TextureManager import Textures
from itblib.Vec import add, smult, sub


class UnitDisplay(PerfSprite):
    """Allows for easier display of a unit on the HUD."""
    IMAGE_SIZE = STANDARD_UNIT_SIZE
    IMAGE_SIZE_BORDER = (2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[0], 2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[1])
    SIZE = (200, IMAGE_SIZE_BORDER[1]+20)
    LABEL_SIZE = (SIZE[0] - IMAGE_SIZE_BORDER[0], HUD.LABEL_HEIGHT)

    def __init__(self):
        super().__init__()
        self.imagepos = (UnitDisplay.SIZE[0] - UnitDisplay.IMAGE_SIZE[0] - HUD.IMAGE_BORDER_WIDTH, HUD.IMAGE_BORDER_WIDTH)
        self.titlepos =           (0, UnitDisplay.LABEL_SIZE[1]*0   + 0)
        self.abilityimagepos =    (0, UnitDisplay.LABEL_SIZE[1]*1   + 1)
        self.abilityphasepos =    (0, UnitDisplay.LABEL_SIZE[1]*2   + 2)
        self.abilitycooldownpos = (0, UnitDisplay.LABEL_SIZE[1]*2.5 + 4)
        self.statuseffectpos =    (0, UnitDisplay.LABEL_SIZE[1]*3   + 4)
        self.defaultimagecolor =   (30,  0,  0, 255)
        self.defaulttextboxcolor = (50, 50, 50, 255)
        self.font = pygame.font.SysFont('latinmodernmono', HUD.FONT_SIZE)
        self.cooldown_font = pygame.font.SysFont('latinmodernmono', 10)
        self.ability_number_font = pygame.font.SysFont('freemono', 10)
        self.image = pygame.Surface(UnitDisplay.SIZE).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0))
        self.displayunit:UnitBaseUI = None
        self.set_displayunit(None)
        self.draw_border()

    def draw_border(self):
        pygame.draw.rect(
            self.image, 
            HUD.IMAGE_BORDER_COLOR, 
            (
                UnitDisplay.SIZE[0] - UnitDisplay.IMAGE_SIZE_BORDER[0],
                0,
                UnitDisplay.IMAGE_SIZE_BORDER[0] - HUD.IMAGE_BORDER_WIDTH/2,
                UnitDisplay.IMAGE_SIZE_BORDER[1] - HUD.IMAGE_BORDER_WIDTH/2,
            ), 
            HUD.IMAGE_BORDER_WIDTH)
    
    def _draw_layout(self):
        self.image.fill(self.defaultimagecolor, (*self.imagepos, *STANDARD_UNIT_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.titlepos,        *UnitDisplay.LABEL_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.abilityimagepos, *UnitDisplay.LABEL_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.abilityphasepos, *UnitDisplay.LABEL_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.statuseffectpos, *UnitDisplay.LABEL_SIZE))
        pygame.draw.line(
            self.image, HUD.IMAGE_BORDER_COLOR, add(self.abilityimagepos,(0,-1)), 
            add(self.abilityimagepos,(UnitDisplay.LABEL_SIZE[0],-1)))
        pygame.draw.line(
            self.image, HUD.IMAGE_BORDER_COLOR, add(self.abilityphasepos,(0,-1)), 
            add(self.abilityphasepos,(UnitDisplay.LABEL_SIZE[0],-1)))
        pygame.draw.line(
            self.image, BLACK, add(self.statuseffectpos, (0,-2)), 
            add(self.statuseffectpos,(UnitDisplay.LABEL_SIZE[0],-2)), 2)

    def set_displayunit(self, unit:UnitBaseUI):
        """Set the new unit to display."""
        self._draw_layout()
        self.displayunit = unit
        if self.displayunit:
            title_text = self.font.render(unit.get_display_name(), True, (255,255,255,255))
            self.image.blit(
                title_text, 
                add(self.titlepos, (0, (self.LABEL_SIZE[1]-title_text.get_height())/2))
            )
            self.image.blits([(blit[0], pygame.Rect(*self.imagepos, *STANDARD_UNIT_SIZE) , blit[2]) for blit in self.displayunit.get_blits()])
            self.display_abilities(unit._parentelement)
            self.display_statuseffects(unit._parentelement)
    
    def update(self, dt):
        self.image.fill(self.defaultimagecolor, (*self.imagepos, *STANDARD_UNIT_SIZE))
        if self.displayunit:
            tfc:TransformComponent = self.displayunit.get_component(TransformComponent)
            unit_pos = add(tfc.get_position(), smult(-.5, STANDARD_UNIT_SIZE))
            self.image.blits(
                [(s,  pygame.Rect(add(sub(g.topleft,unit_pos), self.imagepos), STANDARD_UNIT_SIZE) , l) for s,g,l in self.displayunit.get_blits()]
            )
    
    def display_statuseffects(self, unit:UnitBase):
        self.image.fill((0), (0,100,200,16))
        for i in range(len(unit.statuseffects)):
            texkey = unit.statuseffects[i].name+"Icon"
            spritesheet = Textures.get_spritesheet(texkey)
            if spritesheet:
                self.image.blit(spritesheet[0], (1+i*16, self.statuseffectpos[1]+1))
            else:
                print(f"HUD: Texture {texkey} not found.")
                self.image.fill((255,0,255), (1+i*16,self.statuseffectpos[1]+1,16,16))

    def display_abilities(self, unit:UnitBase):
        """Display the abilities of a unit."""
        abilities = unit.ability_component._abilities
        index = 0
        for ability in abilities:
            if type(ability).__name__ in Textures.abilitytexturemapping.values():
                abilityimage = Textures.get_spritesheet(type(ability).__name__)[0]
                self.image.blit(abilityimage, add(self.abilityimagepos, (17*index, 2)), (0,0,16,16))
            else:
                print(f"HUD: Texture {type(ability).__name__} not found.")

            self.image.fill(PHASECOLORS[ability.phase],
                (*add(self.abilityphasepos, (17*index, 0)), 16, 12)
            )
            if self.displayunit and unit == self.displayunit._parentelement:
                text = str(index+1)
                numberimage = self.ability_number_font.render(text, True, (255,255,255,255), (50,50,50,255))
                self.image.blit(numberimage, add(self.abilityphasepos, (17*(index+1)-numberimage.get_width()-2, 0)))
            
            if ability.primed and ability.remainingcooldown == 0:
                col = (50,100,50,255)
            elif ability.remainingcooldown == 0:
                col = (150,150,150,255)
            else:
                col = (100,50,50,255)
            self.image.fill(col, (*add(self.abilitycooldownpos, (17*index, 0)), 16, 8)
            )
            if self.displayunit and unit == self.displayunit._parentelement:
                text = str(ability.remainingcooldown)
                numberimage = self.cooldown_font.render(text, True, (255,255,255,255), (50,50,50,255))
                self.image.blit(numberimage, add(self.abilitycooldownpos, (17*(index+1)-numberimage.get_width()-2, 0)))

            index += 1

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.image, self.rect, self.image.get_rect())
