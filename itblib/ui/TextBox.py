import pygame.sprite
import pygame.font
from pygame.surface import Surface

class TextBox(pygame.sprite.Sprite):
    def __init__(self, size:"tuple[int,int]", 
                text:str = "AaBbCcDdEeFfGg;:_ÖÄ@ILil",
                bgcolor:"tuple[int,int,int,int]" = (0,0,0,255), 
                textcolor:"tuple[int,int,int,int]" = (255,255,255,255),
                fontsize:int = 20,
                *groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.image = Surface(size)
        self.bgcolor = bgcolor
        self.textcolor =  textcolor
        self.size = size
        self.text = text
        self.font = pygame.font.SysFont('dejavusans', fontsize)
        self.fontimage = self.font.render(self.text, True, self.textcolor, self.bgcolor)
        self.image.fill(self.bgcolor)
        blitx = self.image.get_width() - self.fontimage.get_width()
        blity = self.image.get_height() - self.fontimage.get_height()
        self.image.blit(self.fontimage, (int(blitx/2), int(blity/2)))
