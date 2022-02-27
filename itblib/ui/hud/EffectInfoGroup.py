from typing import Generator

import pygame
from itblib.components.ComponentAcceptor import ComponentAcceptor
from itblib.components.TransformComponent import TransformComponent
from itblib.globals.Colors import WHITE
from itblib.gridelements.EffectsUI import EffectBaseUI
from itblib.input.Input import InputAcceptor
from itblib.ui.widgets.HorizontalLayout import HorizontalLayout
from itblib.ui.IGraphics import IGraphics
from itblib.ui.widgets.TextBox import TextBox


class EffectInfoGroup(ComponentAcceptor, InputAcceptor, IGraphics):
    def __init__(self, width: int) -> None:
        ComponentAcceptor.__init__(self)
        InputAcceptor.__init__(self)
        IGraphics.__init__(self)        
        self.tfc =TransformComponent()
        self.tfc.attach_component(self)
        
        self.effects:list[EffectBaseUI] = []
        self.effect_icons = HorizontalLayout()
        self.effect_icons.tfc.set_transform_target(self)

        self._marker_size = (16,16)
        self.selection_marker = pygame.Surface(self._marker_size).convert_alpha()
        self.selection_marker.fill((0))
        pygame.draw.rect(self.selection_marker, WHITE, (0,0,*self._marker_size), 1)
        self.selection_index = 0
        
        self.title_tb = TextBox("", fontsize=16, bgcolor=(50,50,50), linewidth=width)
        title_tfc = self.title_tb.get_component(TransformComponent)
        title_tfc.relative_position = (0,18)
        title_tfc.set_transform_target(self)
        self.title_tb.update_textbox()
        self.desc_tb = TextBox("", fontsize=16, bgcolor=(50,50,50), linewidth=width)
        self.desc_tb.get_component(TransformComponent).set_transform_target(self.title_tb)

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.effect_icons.get_blits()
        if self.selection_index in range(len(self.effect_icons.children)):
            yield (self.selection_marker, 
                pygame.Rect(self.effect_icons.get_child_pos(self.selection_index), self._marker_size),
                pygame.Rect((0,0), self._marker_size),
            )
        yield from self.title_tb.get_blits()
        yield from self.desc_tb.get_blits()
    
    def handle_key_event(self, event: any) -> bool:
        if event.type == pygame.KEYDOWN and event.mod & pygame.KMOD_CTRL:
            if event.key == pygame.K_LEFT:
                self._move_selection_left()
                return True
            if event.key == pygame.K_RIGHT:
                self._move_selection_right()
                return True
        return super().handle_key_event(event)
    
    def set_effects(self, effects:list[EffectBaseUI]) -> None:
        self.effect_icons.children = [effect.get_icon() for effect in effects]
        self.effects = effects
        self.selection_index = 0
        self._update_title_desc()

    def _update_title_desc(self):
        name = ""
        desc = ""
        if self.selection_index in range(len(self.effects)):
            effect = self.effects[self.selection_index]
            name = effect.get_display_name()
            desc = effect.get_display_description()
        self.title_tb.text = name
        self.title_tb.update_textbox()
        
        desc_pos = (0, self.title_tb.image.get_height()+1)
        self.desc_tb.text = desc
        self.desc_tb.get_component(TransformComponent).relative_position = desc_pos
        self.desc_tb.update_textbox()
    
    def _move_selection_left(self):
        self.selection_index = max(0, self.selection_index-1)
        self._update_title_desc()
    
    def _move_selection_right(self):
        self.selection_index = min(len(self.effect_icons.children)-1, self.selection_index+1)
        self._update_title_desc()
    
    def update(self, delta_time: float) -> None:
        pass