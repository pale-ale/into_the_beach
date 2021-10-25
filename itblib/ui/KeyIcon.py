import pygame
import pygame.sprite
import pygame.draw
import pygame.font

class KeyIcon(pygame.sprite.Sprite):
    BUTTON_LIGHT_GRAY = (150,150,150,255)
    BUTTON_DARK_GRAY = (50,50,50,255)

    def __init__(self, char:str, pos=(0,0), size:"tuple[int,int]"=(30,30), *groups: pygame.sprite.AbstractGroup) -> None:
        self._char = char
        self.image = pygame.Surface(size)
        self.pos = pos
        self.rect = (pos, self.image.get_size())
        self.font = pygame.font.SysFont('dejavusans', 15)
        self.set_char(char)
        super().__init__(*groups)
    
    def set_char(self, char:str):
        self._char = char
        self._draw_bg()
        render = self.font.render(self._char, True, (255,255,255,255))
        self.image.blit(render, ((self.image.get_width() - render.get_width())/2, (self.image.get_height() - render.get_height())/2))
    
    def _draw_bg(self):
        self.image.fill(KeyIcon.BUTTON_DARK_GRAY)
        x,y = self.image.get_size()
        xpad, ypad = 3, 3
        pygame.draw.rect(self.image, KeyIcon.BUTTON_LIGHT_GRAY, (xpad, ypad, x-2*xpad,y-2*ypad), 2, 4)
