"""A collection of Widgets for the UI."""

from typing import TYPE_CHECKING

import pygame
from pygame import Rect, Surface
from pygame.font import Font
from itblib.Vec import IVector2

from itblib.components import ComponentAcceptor, TransformComponent
from itblib.input.Input import InputAcceptor
from itblib.ui.IGraphics import IGraphics
from itblib.globals.Colors import BLACK, DARK_GRAY, GRAY_ACCENT_LIGHT, LIGHT_GRAY, WHITE


if TYPE_CHECKING:
    from typing import Generator, Callable


class Widget(IGraphics, ComponentAcceptor):
    """A Graphical object with a size, hierarchy, transforms, etc."""
    def __init__(self) -> None:
        ComponentAcceptor.__init__(self)
        tfc = TransformComponent()
        tfc.attach_component(self)

    def get_size(self) -> tuple[int, int]:
        return self.image.get_size()

    def get_blits(self) -> "Generator[tuple[Surface, Rect, Rect]]":
        pos = self.get_component(TransformComponent).get_position()
        size = self.image.get_size()
        yield (self.image, Rect(pos.c, self.image.get_size()), ((0, 0), size))

    @property
    def parent(self) -> "ComponentAcceptor|None":
        """
        Widgets calculate their global positions as their parent's position
        + local offset
        """
        parent_tfc = self.get_component(TransformComponent).parent_transform_component
        return parent_tfc.owner if parent_tfc else None

    @property
    def position(self) -> IVector2:
        """The local offset of a Widget"""
        return self.get_component(TransformComponent).relative_position

    @parent.setter
    def parent(self, new_parent: "ComponentAcceptor"):
        self.get_component(TransformComponent).set_transform_target(new_parent)

    @position.setter
    def position(self, new_position: IVector2):
        assert isinstance(new_position, IVector2)
        self.get_component(TransformComponent).relative_position = new_position


class TextBox(Widget):
    """
    Since alpha=0 in text renders is currently broken,
    use (0,0,0,0) as color to be removed.
    """
    def __init__(
            self,
            text: str = "AaBbCcDdEeFfGg;:_ÖÄ@ILil",
            bgcolor: "tuple[int,int,int,int]" = (0, 0, 0, 255),
            textcolor: "tuple[int,int,int,int]" = (255, 255, 255, 255),
            fontsize: int = 16,
            pos: IVector2 = IVector2(0, 0),
            linewidth: int = 150,
            lineheight: int = None,
            oneline: bool = False
            ) -> None:
        super().__init__()
        self.font = Font("HighOne.ttf", fontsize)
        self.textcolor = textcolor
        self.bgcolor = bgcolor
        self.linewidth = linewidth
        self.oneline = oneline
        self.lineheight = lineheight or self.font.get_height()
        self.image: Surface = None
        assert isinstance(pos, IVector2)
        self.position = pos
        self.text = text
        self.update_textbox()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text: str):
        self._text = new_text
        self.update_textbox()

    def update_textbox(self):
        """After changing the values, generate a new image for the textbox."""
        if self.oneline:
            text = self.text
            textsurf = self.font.render(
                text,
                False,
                self.textcolor,
                self.bgcolor)
            size = (textsurf.get_width(), self.lineheight)
            self.image = Surface(size)
            self.image.fill(self.bgcolor)
            border = (textsurf.get_height()-self.lineheight)*.5
            subsurf = textsurf.subsurface((
                0,
                border,
                textsurf.get_width(),
                textsurf.get_height()-border
            )).convert_alpha()
            self.image.blit(subsurf, (1, 0))
        else:
            linebreak_text = self._break_lines_font(
                self.text,
                self.font,
                self.linewidth
            ).splitlines()
            size = (
                self.linewidth,
                max(self.lineheight, len(linebreak_text)*self.lineheight)
            )
            self.image = Surface(size)
            self.image.fill(self.bgcolor)
            for i, line in enumerate(linebreak_text):
                textsurf = self.font.render(
                    line,
                    False,
                    self.textcolor,
                    self.bgcolor
                )
                border = (textsurf.get_height()-self.lineheight)*.5
                subsurf = textsurf.subsurface((
                    0,
                    border,
                    textsurf.get_width(),
                    textsurf.get_height()-border
                )).convert_alpha()
                self.image.blit(subsurf, (1, i*self.lineheight))
        self.image.set_colorkey((0, 0, 0, 0))

    def _break_lines_font(
            self,
            text: str,
            font: Font,
            textbox_width: int
            ) -> str:
        """
        Break a text at spaces and newlines,
        so that the line rendered with the specified font
        will not exceed the width.
        """
        def get_str_font_len(text: str, font: Font):
            """Calculate len of a string based on it's font."""
            return font.render(text, False, (0)).get_width()
        lines: list[str] = []
        split_text = text.split()
        space_width = get_str_font_len(" ", font)
        current_line = ""
        current_line_width = get_str_font_len(current_line, font)
        for word in split_text:
            word_len = get_str_font_len(word, font)
            if current_line_width + word_len + (space_width if current_line else 0) > textbox_width:
                lines.append(current_line.strip())
                current_line = word
            else:
                current_line += " " + word
            current_line.strip()
            current_line_width = get_str_font_len(current_line, font)
        lines.append(current_line.strip())
        return '\n'.join(lines)


class KeyIcon(Widget):
    """
    The KeyIcon Widget can be used to display a single
    char with a keyboard-key style.
    """
    BUTTON_LIGHT_GRAY = (150, 150, 150, 255)

    def __init__(
            self,
            text: str,
            pos: IVector2 = IVector2(0, 0),
            size: IVector2 = IVector2(32, 32),
            pressed: bool = False,
            enabled=True,
            fontsize=32
            ) -> None:
        super().__init__()
        self._text = TextBox(text, bgcolor=DARK_GRAY, fontsize=32)
        self.image = Surface(size.c).convert_alpha()
        self.font = Font('HighOne.ttf', fontsize)
        self._outer_border = IVector2(3, 3)
        self._inner_border = IVector2(2, 2)
        self._pressed = pressed
        self._enabled = enabled
        self.char = text
        self.position = pos

    @property
    def char(self):
        return self._char

    @property
    def pressed(self):
        return self._pressed
    
    @property
    def enabled(self):
        return self._enabled

    @char.setter
    def char(self, new_char: str):
        self._char = new_char
        self._redraw()

    @pressed.setter
    def pressed(self, new_presed: bool):
        self._pressed = new_presed
        self._redraw()
    
    @enabled.setter
    def enabled(self, new_enabled: bool):
        self._enabled = new_enabled
        self._redraw()

    def _redraw(self):
        char_surface = self.font.render(self._char, True, WHITE)
        char_size = char_surface.get_size()
        size = IVector2(*self.image.get_size())
        self.image.fill(0)

        inner = self._outer_border + self._inner_border
        outer_rect_pos = self._outer_border
        outer_rect_size = size - 2 * self._outer_border
        inner_rect_pos = self._outer_border + self._inner_border
        inner_rect_size = size - 2 * inner
        if self.pressed:
            outer_rect_pos += IVector2(0, self._outer_border.y-1)
            inner_rect_pos += IVector2(0, self._outer_border.y-1)
        else:
            lower_rect_pos = self._outer_border + IVector2(0, self._outer_border.y-1)
            lower_rect_size = size - 2 * self._outer_border
            lower_rect = Rect(lower_rect_pos.c, lower_rect_size.c)
            pygame.draw.rect(self.image, LIGHT_GRAY, lower_rect, 2, 4)
        
        outer_rect = Rect(outer_rect_pos.c, outer_rect_size.c)
        inner_rect = Rect(inner_rect_pos.c, inner_rect_size.c)
        self.image.fill(DARK_GRAY if self._enabled else (GRAY_ACCENT_LIGHT), inner_rect)
        pygame.draw.rect(self.image, KeyIcon.BUTTON_LIGHT_GRAY, outer_rect, 2, 4)
        self.image.blit(char_surface, (
            (self.image.get_width() - char_size[0])/2+1, 
            (self.image.get_height() - char_size[1])/2+(self._outer_border.y-1 if self.pressed else 0))
        )


class GridSelection(InputAcceptor, Widget):
    """Display a number of surfaces, aligned by rows and columns in a grid-like manner."""
    def __init__(self) -> None:
        Widget.__init__(self)
        InputAcceptor.__init__(self)
        self._x_max_elements = 6
        self._x_padding = 2
        self._y_padding = 2
        self._selectable_count = 1
        self._duplicate_count = 1
        self._size = IVector2(500, 300)
        self._elem_size = IVector2(64, 64)
        self._cursor_colour = (0, 0, 255)
        self._cursorpos: IVector2 = IVector2(0,0)
        self._lines = 0
        self._cursor_frame_thickness = 2
        self._element_background = (150, 50, 150)
        self._selections: dict[int:int] = {}
        self._elem_count = 0
        self.image = Surface(self._size.c)
        self.selection_update_callback: "Callable[[list[int]],None]|None" = None

    @property
    def data_source(self):
        return self._data_source

    def set_data_source(self, new_data_source: "Callable[[int], pygame.Surface]", elem_count: int):
        """Set the mapping funciton used to obtain a Surface from an index."""
        self._data_source = new_data_source
        self._elem_count = elem_count
        self._selections.clear()
        self._redraw()

    def set_properties(self, 
                    selectable_count:    "int|None" = None,
                    duplicate_count:     "int|None" = None,
                    size:     "IVector2|None" = None,
                    paddings: "IVector2|None" = None,
                    elem_size:"IVector2|None" = None,
                    cursor_colour:"tuple[int,int,int]|None" = None):
        """Convenience function to set multiple properties at once insetad of chaining."""
        if selectable_count is not None:
            self._selectable_count = selectable_count
        if duplicate_count is not None:
            self._duplicate_count = duplicate_count
        if size is not None:
            self._size =  size
        if paddings is not None:
            self._x_padding, self._y_padding = paddings
        if elem_size is not None:
            self._elem_size = elem_size
        if cursor_colour is not None:
            self._cursor_colour = cursor_colour
        self._x_max_elements = int(self._size.x/self._elem_size.x)
        self._redraw()

    def handle_key_event(self, event: any) -> bool:
        if event.key == pygame.K_UP:
            self._update_cursor_pos((0, -1))
            return True
        elif event.key == pygame.K_RIGHT:
            self._update_cursor_pos((1, 0))
            return True
        elif event.key == pygame.K_DOWN:
            self._update_cursor_pos((0, 1))
            return True
        elif event.key == pygame.K_LEFT:
            self._update_cursor_pos((-1, 0))
            return True
        elif event.key == pygame.K_RETURN:
            i = self._cursorpos.y * self._x_max_elements + self._cursorpos.x
            if self._get_elem_copy_count(i) < self._duplicate_count:
                self._incr_elem_copy_count(i)
                self._update_cursor_pos((0, 0))
            return True
        elif event.key == pygame.K_BACKSPACE:
            i = self._cursorpos.y * self._x_max_elements + self._cursorpos.x
            if i in self._selections:
                self._decr_elem_copy_count(i)
                self._update_cursor_pos((0, 0))
            return True
        return super().handle_key_event(event)

    def _update_cursor_pos(self, delta: "IVector2|tuple[int,int]"):
        x,y = self._cursorpos + delta
        safe_x = max(min(x,self._x_max_elements-1), 0)
        safe_y = max(min(y,self._lines-1), 0)
        self._cursorpos = IVector2(safe_x, safe_y)
        self._redraw()

    def _c_to_s(self, coord: IVector2):
        x,y = coord
        sx = x * (self._elem_size.x + self._x_padding) + self._x_padding + self._cursor_frame_thickness
        sy = y * (self._elem_size.y + self._y_padding) + self._y_padding + self._cursor_frame_thickness
        return IVector2(sx, sy)

    def _redraw(self):
        self.image = Surface(self._size.c)
        self.image.fill((0), ((0,0),self._size.c))
        for i in range(self._elem_count):
            x = int(i%self._x_max_elements)
            y = int(i/self._x_max_elements)
            data_elem = self._data_source(i)
            spos = self._c_to_s((x,y))
            size = IVector2(*data_elem.get_size())
            self.image.fill((0), (spos.c, size.c))
            self.image.blit(data_elem, (spos.c, size.c), ((0, 0), size.c))
            selection_count = TextBox(
                "I"*self._get_elem_copy_count(i),
                pos=spos,
                fontsize=10)
            self.image.blit(selection_count.image, (spos.c, size.c), ((0, 0), size.c))

        thickness_offset = IVector2(self._cursor_frame_thickness)
        cursor_pos = self._c_to_s(self._cursorpos) - thickness_offset
        cursor_size = self._elem_size + 2 * thickness_offset + IVector2(1)
        rect = Rect(cursor_pos.c, cursor_size.c)
        pygame.draw.rect(self.image, self._cursor_colour, rect, self._cursor_frame_thickness, 5)

    def _get_elem_copy_count(self, elementindex: int) -> int:
        return self._selections.get(elementindex, 0)

    def _incr_elem_copy_count(self, elementindex: int):
        if elementindex in self._selections:
            self._selections[elementindex] += 1
        else:
            self._selections[elementindex] = 1
        if self.selection_update_callback:
            self.selection_update_callback(self._selections)

    def _decr_elem_copy_count(self, elementindex: int):
        self._selections[elementindex] -= 1
        if self._selections[elementindex] <= 0:
            self._selections.pop(elementindex)
        if self.selection_update_callback:
            self.selection_update_callback(self._selections)
