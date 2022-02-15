import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent


class TextBox(pygame.sprite.Sprite, ComponentAcceptor):
    """Since alpha=0 in text renders is currently broken, use (0,0,0,0) as color to be removed."""
    def __init__(self, 
                text:str = "AaBbCcDdEeFfGg;:_ÖÄ@ILil",
                bgcolor:"tuple[int,int,int,int]" = (0,0,0,255), 
                textcolor:"tuple[int,int,int,int]" = (255,255,255,255),
                fontsize:int = 16,
                pos:"tuple[int,int]" = (0,0),
                linewidth:int = 150,
                lineheight:int = None,
                *groups: pygame.sprite.AbstractGroup) -> None:
        ComponentAcceptor.__init__(self)
        tfc = TransformComponent()
        tfc.attach_component(self)
        self.text = text
        self.font = pygame.font.Font("HighOne.ttf", fontsize)
        self.textcolor = textcolor
        self.bgcolor = bgcolor
        self.linewidth = linewidth
        self.lineheight = lineheight if lineheight else self.font.get_height() - 2*(fontsize/8)
        self.image:pygame.Surface = None
        self.rect:pygame.Rect = pygame.Rect(pos, (0,0))
        pygame.sprite.Sprite.__init__(self, *groups)
        self.update_textbox()

    def update_textbox(self):
        """After changing the values, generate a new image for the textbox."""
        linebreak_text = self._break_lines_font(self.text, self.font, self.linewidth).splitlines()
        self.image = pygame.Surface((self.linewidth, len(linebreak_text)*self.lineheight))
        self.image.fill(self.bgcolor)
        for i,line in enumerate(linebreak_text):
            textsurf = self.font.render(line, False, self.textcolor, self.bgcolor)
            border = (textsurf.get_height()-self.lineheight)*.5
            subsurf = textsurf.subsurface((0,border, textsurf.get_width(), textsurf.get_height()-border)).convert_alpha()
            self.image.blit(subsurf, (1, i*self.lineheight))
        self.image.set_colorkey((0,0,0,0))
        self.rect = pygame.Rect(self.get_component(TransformComponent).get_position(), self.image.get_size())
    
    def _break_lines_font(self, text:str, font:pygame.font.Font, textbox_width:int) -> str:
        """Break a text at spaces and newlines, so that the line rendered with the specified font will not exceed the width."""
        def get_str_font_len(text:str, font:pygame.font.Font):
            """Calculate the length of a string based on the font it is rendered with."""
            return font.render(text, False, (0)).get_width()
        
        lines:list[str] = []
        split_text = text.split()
        space_width = get_str_font_len(" ", font)
        current_line = ""
        current_line_width = get_str_font_len(current_line, font)
        for word in split_text:
            word_len = get_str_font_len(word, font)
            if current_line_width + word_len + (space_width if current_line != "" else 0) > textbox_width:
                lines.append(current_line.strip())
                current_line = word
            else:
                current_line += " " + word
            current_line.strip()
            current_line_width = get_str_font_len(current_line, font)
        lines.append(current_line.strip())
        return '\n'.join(lines)

