import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent


class TextBox(pygame.sprite.Sprite, ComponentAcceptor):
    """Since alpha=0 in text renders is currently broken, use (0,0,0,0) as color to be removed."""
    def __init__(self, 
                text:str = "AaBbCcDdEeFfGg;:_ÖÄ@ILil",
                bgcolor:"tuple[int,int,int,int]" = (0,0,0,255), 
                textcolor:"tuple[int,int,int,int]" = (255,255,255,255),
                fontsize:int = 20,
                pos:"tuple[int,int]" = (0,0),
                linewidth:int = 150,
                lineheight:int = 15,
                *groups: pygame.sprite.AbstractGroup) -> None:
        ComponentAcceptor.__init__(self)
        tfc = TransformComponent()
        tfc.attach_component(self)
        self.text = text
        self.textcolor = textcolor
        self.bgcolor = bgcolor
        self.linewidth = linewidth
        self.lineheight = lineheight
        self.image = pygame.Surface((100,100))
        self.font = pygame.font.SysFont('firamono', fontsize)
        self.rect = pygame.Rect(*pos, *self.image.get_size())
        pygame.sprite.Sprite.__init__(self, *groups)
        self.update_textbox()

    def update_textbox(self):
        """After changing the values, generate a new image for the textbox."""
        linebreak_text = self._break_lines_font(self.text, self.font, self.linewidth).splitlines()
        self.image = pygame.Surface((self.linewidth, len(linebreak_text)*self.lineheight))
        self.image.fill(self.bgcolor)
        for i,line in enumerate(linebreak_text):
            self.image.blit(self.font.render(line, True, self.textcolor, self.bgcolor).copy().convert_alpha(), (0, i*self.lineheight))
        self.image.set_colorkey((0,0,0,0))
        self.rect.size = self.image.get_size()
    
    def _break_lines_font(self, text:str, font:pygame.font.Font, width:int) -> str:
        """Will only work properly with monospaced fonts."""
        letterwidth = font.render("x", False, (0), (0)).get_width()+1
        return self._break_lines(text, max(width/letterwidth, 5))
    
    def _break_lines(self, text:str, letters_per_line:int) -> str:
        lines:list[str] = []
        split_text = text.split()
        line = ""
        current_line_letter_count = len(line)
        for word in split_text:
            wordlen = len(word)
            if current_line_letter_count + wordlen > letters_per_line:
                lines.append(line.strip())
                current_line_letter_count = 0
                line = word
            else: 
                line += " " + word
            line.strip()
            current_line_letter_count += wordlen
        lines.append(line.strip())
        return '\n'.join(lines)

