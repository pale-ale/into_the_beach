from typing import Callable

import pygame
from itblib.input.Input import InputAcceptor
from itblib.ui.widgets.TextBox import TextBox
from itblib.ui.widgets.Widget import Widget
from itblib.Vec import add, smult, sub


class GridSelection(InputAcceptor, Widget):
    """Display a number of surfaces, aligned by rows and columns in a grid-like manner."""
    def __init__(self) -> None:
        InputAcceptor.__init__(self)
        Widget.__init__(self)
        self._x_max_elements = 6
        self._x_padding = 2
        self._y_padding = 2
        self._selectable_count = 1
        self._duplicate_count = 1
        self._size = (500,300)
        self._elem_size = (64,64)
        self._cursor_colour = (0,0,255)

        self._cursorpos:tuple[int,int] = (0,0)
        self._lines = 0
        self._cursor_frame_thickness = 2
        self._element_background = (150,50,150)
        self._selections:dict[int:int] = {}
        self._elem_count = 0
        self.image = pygame.Surface(self._size)
        self.selection_update_callback:"Callable[[list[int]],None]|None" = None
    
    @property
    def data_source(self):
        return self._data_source
    
    def set_data_source(self, new_data_source:Callable[[int], pygame.Surface], elem_count:int):
        """Set the mapping funciton used to obtain a Surface from an index."""
        self._data_source = new_data_source
        self._elem_count = elem_count
        self._selections.clear()
        self._redraw()

    def setProperties(self, 
                    selectable_count:    "int|None" = None,
                    duplicate_count:     "int|None" = None,
                    size:     "tuple[int,int]|None" = None,
                    paddings: "tuple[int,int]|None" = None,
                    elem_size:"tuple[int,int]|None" = None,
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
        self._x_max_elements = int(self._size[0]/self._elem_size[0])
        self._redraw()
    
    def handle_key_event(self, event: any) -> bool:
        if event.key == pygame.K_UP:
            self._update_cursor_pos((0,-1))
            return True
        elif event.key == pygame.K_RIGHT:
            self._update_cursor_pos((1,0))
            return True
        elif event.key == pygame.K_DOWN:
            self._update_cursor_pos((0,1))
            return True
        elif event.key == pygame.K_LEFT:
            self._update_cursor_pos((-1,0))
            return True
        elif event.key == pygame.K_RETURN:
            i = self._cursorpos[1]*self._x_max_elements + self._cursorpos[0]
            if self._get_elem_copy_count(i) < self._duplicate_count:
                self._incr_elem_copy_count(i)
                self._update_cursor_pos((0,0))
            return True
        elif event.key == pygame.K_BACKSPACE:
            i = self._cursorpos[1]*self._x_max_elements + self._cursorpos[0]
            if i in self._selections.keys():
                self._decr_elem_copy_count(i)
                self._update_cursor_pos((0,0))
            return True
        return super().handle_key_event(event)
    
    def _update_cursor_pos(self, delta:"tuple[int,int]"):
        x,y = add(self._cursorpos, delta)
        safe_x = max(min(x,self._x_max_elements-1), 0)
        safe_y = max(min(y,self._lines-1), 0)
        self._cursorpos = (safe_x, safe_y)
        self._redraw()
    
    def _c_to_s(self, c:"tuple[int,int]"):
        x,y = c
        sx = x * (self._elem_size[0]+self._x_padding) + self._x_padding + self._cursor_frame_thickness
        sy = y * (self._elem_size[1]+self._y_padding) + self._y_padding + self._cursor_frame_thickness
        return (sx, sy)
    
    def _redraw(self):
        self.image = pygame.Surface(self._size)
        self.image.fill((0), ((0,0),self._size))
        for i in range(self._elem_count):
            x = int(i%self._x_max_elements)
            y = int(i/self._x_max_elements)
            data_elem = self._data_source(i)
            spos = self._c_to_s((x,y))
            size = data_elem.get_size()
            self.image.fill((0), (spos, size))
            self.image.blit(data_elem, (spos,size), ((0,0),size))
            selection_count = TextBox(
                "I"*self._get_elem_copy_count(i), 
                pos=spos, 
                fontsize=10)
            self.image.blit(selection_count.image, (spos,size), ((0,0),size))

        thickness_offset = (self._cursor_frame_thickness, self._cursor_frame_thickness)
        cursor_pos = sub(self._c_to_s(self._cursorpos), thickness_offset)
        cursor_size = add(self._elem_size, smult(2, thickness_offset), (1,1))
        rect = pygame.Rect(cursor_pos, cursor_size)
        pygame.draw.rect(self.image, self._cursor_colour, rect, self._cursor_frame_thickness, 5)
    
    def _get_elem_copy_count(self, elementindex:int) -> int:
        return self._selections.get(elementindex, 0)
    
    def _incr_elem_copy_count(self, elementindex:int):
        if elementindex in self._selections.keys():
            self._selections[elementindex] += 1
        else:
            self._selections[elementindex] = 1
        if self.selection_update_callback:
            self.selection_update_callback(self._selections)
    
    def _decr_elem_copy_count(self, elementindex:int):
        self._selections[elementindex] -= 1
        if self._selections[elementindex] <= 0:
            self._selections.pop(elementindex)
        if self.selection_update_callback:
            self.selection_update_callback(self._selections)
