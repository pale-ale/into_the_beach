import pygame
import pygame.draw
import pygame.font
from itblib.globals.Colors import DARK_GRAY, LIGHT_GRAY
from itblib.Vec import add, sub, smult

from itblib.ui.widgets.Widget import Widget
from itblib.ui.widgets.TextBox import TextBox

class KeyIcon(Widget):
    """The KeyIcon Widget can be used to display a single char with a keyboard-key style."""
    BUTTON_LIGHT_GRAY = (150,150,150,255)

    def __init__(self, text:str, pos=(0,0), size:"tuple[int,int]"=(32,32), pressed:bool = False, fontsize=32) -> None:
        super().__init__()
        self._text = TextBox(text, bgcolor=DARK_GRAY, fontsize=32)
        self.image = pygame.Surface(size).convert_alpha()
        self.font = pygame.font.Font('HighOne.ttf', fontsize)
        self._outer_border = (3,3)
        self._inner_border = (2,2)
        self._pressed = pressed
        self.char = text
        self.position = pos
    
    @property
    def char(self):
        return self._char
    
    @property
    def pressed(self):
        return self._pressed

    @char.setter
    def char(self, new_char:str):
        self._char=new_char
        self._redraw()
    
    @pressed.setter
    def pressed(self, new_presed:bool):
        self._pressed = new_presed
        self._redraw()
    
    def _redraw(self):
        char_surface = self.font.render(self._char, True, (255,255,255,255))
        char_size = char_surface.get_size()
        size = self.image.get_size()
        self.image.fill((0,0,0,0))
        if self.pressed:
            outer_rect = (add(self._outer_border, (0,self._outer_border[1]-1)), sub(size, smult(2, self._outer_border)))
            inner = add(self._outer_border, self._inner_border)
            inner_rect = (add(inner, (0,self._outer_border[1]-1)), sub(size, smult(2, inner)))
        else:
            outer_rect = (self._outer_border, sub(size, smult(2, self._outer_border)))
            inner = add(self._outer_border, self._inner_border)
            inner_rect = (inner, sub(size, smult(2, inner)))
            lower_rect = (add(self._outer_border, (0,self._outer_border[1]-1)), sub(size, smult(2, self._outer_border)))
            pygame.draw.rect(self.image, LIGHT_GRAY, lower_rect, 2, 4)
        self.image.fill(DARK_GRAY, inner_rect)
        pygame.draw.rect(self.image, KeyIcon.BUTTON_LIGHT_GRAY, outer_rect, 2, 4)
        self.image.blit(char_surface, (
            (self.image.get_width() - char_size[0])/2+1, 
            (self.image.get_height() - char_size[1])/2+(self._outer_border[1]-1 if self.pressed else 0))
        )
