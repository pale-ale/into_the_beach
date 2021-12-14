from pygame import Rect
import pygame.sprite
import pygame.font
import pygame.surface

class TextBox(pygame.sprite.Sprite):
    def __init__(self, 
                text:str = "AaBbCcDdEeFfGg;:_ÖÄ@ILil",
                bgcolor:"tuple[int,int,int,int]" = (0,0,0,255), 
                textcolor:"tuple[int,int,int,int]" = (255,255,255,255),
                fontsize:int = 20,
                pos:"tuple[int,int]" = (0,0),
                *groups: pygame.sprite.AbstractGroup) -> None:
        font = pygame.font.SysFont('firamono', fontsize)
        textsurf = font.render(text, True, textcolor)
        textsurf.set_alpha(textcolor[3])
        self.image = pygame.surface.Surface(textsurf.get_size()).convert_alpha()
        self.image.fill(bgcolor)
        self.image.blit(textsurf, (0,0))
        self.rect = Rect(*pos, *self.image.get_size())
        super().__init__(*groups)
