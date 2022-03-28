"""Contains many on-screen compound elements that make up the HUD."""

from typing import TYPE_CHECKING

import pygame
import pygame.font
import pygame.image
import pygame.sprite
import pygame.transform
from itblib.components import TransformComponent
from itblib.Game import Session
from itblib.globals.Colors import (BLACK, DARK_GRAY, GRAY_ACCENT_DARK,
                                   GRAY_ACCENT_LIGHT, IMAGE_BACKGROUND,
                                   PHASECOLORS, WHITE)
from itblib.globals.Constants import (HUD, PHASE_DURATIONS, PREVIEWS,
                                      STANDARD_TILE_SIZE, STANDARD_UNIT_SIZE)
from itblib.gridelements.TilesUI import TileBaseUI
from itblib.gridelements.world_effects import EffectStartingArea
from itblib.input.Input import InputAcceptor
from itblib.Log import log
from itblib.net.NetEvents import NetEvents
from itblib.ui.animations import Animation
from itblib.ui.animations import PlayerVersusAnimation
from itblib.ui.GridUI import GridUI
from itblib.ui.hud.ability_preview_display import AbilityPreviewDisplay
from itblib.ui.IGraphics import IGraphics
from itblib.ui.TextureManager import Textures
from itblib.ui.widgets.layout import HorizontalLayoutSurface
from itblib.ui.widgets.ui_widget import TextBox, Widget
from itblib.Vec import add, sub

if TYPE_CHECKING:
    from typing import Generator

    from itblib.gridelements.ui_effect import EffectBaseUI
    from itblib.gridelements.units.UnitBase import UnitBase
    from itblib.gridelements.UnitsUI import UnitBaseUI
    from itblib.abilities.ui_abilities import AbilityBaseUI


class Hud(IGraphics, InputAcceptor):
    """
    The HUD is used to display most information, like a unit's HP, abilities, cooldowns,
    the tile it is on, it's effects, etc.
    """

    def __init__(self, size:"tuple[int,int]", gridui:GridUI, playerid:int, session:Session):
        IGraphics.__init__(self)
        InputAcceptor.__init__(self)
        self.rect = pygame.Rect(0,0,*size)
        self.selected_unit:"UnitBase|None" = None
        self.selected_unitui:"UnitBaseUI|None" = None
        self.gridui = gridui
        self.gridui.phase_change_callback = self.update_phase
        self.font = pygame.font.Font('HighOneMono.ttf', 32)
        self._cursorgridpos = (0,0)
        self._cursorscreenpos = (0,0)
        self.displayscale = 2
        self._unitdisplay = UnitDisplay()
        self._tiledisplay = TileDisplay()
        self.abilitydisplay = AbilityDisplay()
        self.register_input_listeners(self._tiledisplay)
        self._ability_preview_display = AbilityPreviewDisplay(gridui)
        self._unitdisplay.rect.topleft = (self.rect.width - HUD.ELEM_WIDTH, 0)
        self.playerid = playerid
        self.session = session
        self.blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
        self.owner_blits:"list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]" = []
        self.cursor_blit = None

    def update_phase(self, newphase:int):
        if newphase == 1:
            self.selected_unit = None
            self._unitdisplay.set_displayunit(self.selected_unitui)

    #pylint: disable=missing-function-docstring
    def handle_key_event(self, event) -> bool:
        if self.selected_unit and self.selected_unit.handle_key_event(event):
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.targetconfirm(self._cursorgridpos)
                return True
            if event.key == pygame.K_SPACE:
                self.select_unit(self.gridui.grid.get_unit(self._cursorgridpos))
                return True
            if event.key == pygame.K_ESCAPE:
                if self.selected_unit:
                    self.select_unit(None)
                    return True
                else:
                    NetEvents.snd_netplayerleave(self.playerid)
                    return True
        return super().handle_key_event(event)

    def select_unit(self, unit:"UnitBase|None"):
        """
        Mark a unit as selected, displaying it's stats in greater detail and allowing ability use.
        """
        if unit != self.selected_unit:
            if self.selected_unit:
                self.selected_unit.ability_component.on_deselect()
        if unit:
            if unit.ownerid == self.playerid:
                self.selected_unit = unit
                self.selected_unitui = self.gridui.get_unitui(self._cursorgridpos)
                unit.ability_component.on_select()
        else:
            self.selected_unit = None

    def targetconfirm(self, position:"tuple[int,int]"):
        """
        Forward the position of the selected target to the selected unit's hooks or spawn a unit.
        """
        player = self.session.get_player(self.playerid)
        if self.gridui.grid.phase == 0 and len(player.initialunitids) > 0 and\
        self.gridui.grid.is_space_empty(False, position):
            for effect in self.gridui.grid.get_worldeffects(position):
                if isinstance(effect, EffectStartingArea) and effect.ownerid == self.playerid:
                    unit_id = player.initialunitids.pop(0)
                    self.gridui.grid.request_add_unit(position, unit_id, self.playerid)
        elif self.selected_unit:
            self.selected_unit.ability_component.on_confirm_target(position)
            self._unitdisplay.set_displayunit(self.selected_unitui)

    def activate_ability(self, slot:int):
        """Activate the ability with the according number, and deselect all others."""
        if self.selected_unit and self.gridui.grid.phase == 1:
            self.selected_unit.ability_component.on_deselect()
            self.selected_unit.ability_component.on_activate_ability(slot-1)
            self._unitdisplay.set_displayunit(self.selected_unitui)

    def get_unit_ability_preview_blits(self):
        """Retrieve ability previews blits of a unit, e.g. movement and targeting info."""
        for unit in self.gridui.grid.units:
            if unit:
                self._ability_preview_display.unit = unit
                yield from self._ability_preview_display.get_blits()

    def _get_phase_timer_blit(self):
        maxphasetime = PHASE_DURATIONS.DURATIONS[self.gridui.grid.phase]
        currentphasetime = self.gridui.grid.phasetime
        formatted_time = str(round(max(0.0,maxphasetime-currentphasetime), 1)).zfill(4)
        timer_surface = self.font.render(formatted_time, True, WHITE, DARK_GRAY).convert()
        t_x, t_y = timer_surface.get_size()
        player = self.session.get_player(self.playerid)
        player_color = player.color if player else (50,50,50,255)
        phase_color = PHASECOLORS[self.gridui.grid.phase]
        pygame.draw.line(timer_surface, player_color, (0,     0), (t_x,     0), 1)
        pygame.draw.line(timer_surface,        BLACK, (0,     1), (t_x,     1), 2)
        pygame.draw.line(timer_surface,        BLACK, (0, t_y-3), (t_x, t_y-3), 2)
        pygame.draw.line(timer_surface,  phase_color, (0, t_y-1), (t_x, t_y-1), 1)
        timer_pos = ((self.rect.width - t_x)/2, 10)
        yield (timer_surface, pygame.Rect(*timer_pos, t_x, t_y), pygame.Rect(0,0,t_x-2,t_y))

    def player_won(self, playerid:int):
        if self.playerid == playerid:
            log("\nI Won!\n", 2)
        else:
            log("\nI Lost!\n", 2)

    def _update_display_unit_if_necessary(self):
        grid_unit = self.gridui.get_unitui(self._cursorgridpos)
        display_unit = self._unitdisplay.displayunitui
        if grid_unit is not display_unit:
            self._unitdisplay.set_displayunit(grid_unit)

    def update_cursor(self, position:"tuple[int,int]|None"=None):
        """Forward the new cursor position to a unit's according hooks"""
        position = position if position else self._cursorgridpos
        self._tiledisplay.tile = self.gridui.get_tileui(position)
        self._tiledisplay.effects = self.gridui.get_tile_effectsui(position)
        self._unitdisplay.set_displayunit(self.gridui.get_unitui(position))
        self._cursorgridpos = position
        self._cursorscreenpos = self.gridui.transform_grid_screen(position)
        if self.cursor_blit:
            self.blits.remove(self.cursor_blit)
        cursor_spritesheet = Textures.get_spritesheet(PREVIEWS[0])
        if cursor_spritesheet:
            self.cursor_blit = (
                cursor_spritesheet[0],
                pygame.Rect(*self._cursorscreenpos,64,64),
                pygame.Rect(0,0,64,64)
            )
        self.blits.append(self.cursor_blit)
        if self.selected_unit:
            self.selected_unit.ability_component.on_update_cursor(position)

    def on_start_game(self):
        p_1, p_2 = self.session._players.values()
        self.abilitydisplay.play_simple_anim(PlayerVersusAnimation(p_1, p_2, *self.rect.size))

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.blits
        yield from self._get_phase_timer_blit()
        yield from self._tiledisplay.get_blits()
        yield from self._unitdisplay.get_blits()
        yield from self.get_unit_ability_preview_blits()
        yield from self.abilitydisplay.get_blits()

    def update(self, delta_time: float) -> None:
        self._update_display_unit_if_necessary()
        self._tiledisplay.update(delta_time)
        self._unitdisplay.update(delta_time)
        self.abilitydisplay.update(delta_time)


class TileDisplay(Widget, InputAcceptor):
    """Displays various anformation about a tile and it's current effects."""
    IMAGE_SIZE_BORDER = (
        2*HUD.IMAGE_BORDER_WIDTH + HUD.TILEDISPLAY.IMAGE_SIZE[0],
        2*HUD.IMAGE_BORDER_WIDTH + HUD.TILEDISPLAY.IMAGE_SIZE[1]
    )
    SIZE = (200,IMAGE_SIZE_BORDER[1])
    LABEL_SIZE = (SIZE[0] - IMAGE_SIZE_BORDER[0] - 2, HUD.LABEL_HEIGHT)

    def __init__(self):
        Widget.__init__(self)
        InputAcceptor.__init__(self)

        self._imagepos = (HUD.IMAGE_BORDER_WIDTH, HUD.IMAGE_BORDER_WIDTH)
        self._tilenamepos = (TileDisplay.IMAGE_SIZE_BORDER[0],HUD.IMAGE_BORDER_WIDTH)
        self._tiledescpos = None
        self._tileseffectpos = None

        self._tilenametextbox = TextBox(
            fontsize=32,
            bgcolor=GRAY_ACCENT_DARK,
            linewidth=TileDisplay.LABEL_SIZE[0],
            lineheight=20
        )
        self._tiledesctextbox = TextBox(
            fontsize=15,
            bgcolor=GRAY_ACCENT_DARK,
            linewidth=TileDisplay.LABEL_SIZE[0],
            lineheight=10
        )
        self._effectdisplay = EffectInfoGroup(TileDisplay.LABEL_SIZE[0])
        self._effectdisplay.parent = self
        self.register_input_listeners(self._effectdisplay)

        self._sub_blits:list[tuple[pygame.Surface, pygame.Rect, pygame.Rect]] = []
        self.image = pygame.Surface((200,100)).convert_alpha()
        self._rect = self.image.get_rect()
        self.image.fill((0))
        self.tile:"TileBaseUI" = None
        self.effects:"list[EffectBaseUI]" = []
        self._draw_border()

    @property
    def tile(self):
        return self._tile

    @property
    def effects(self):
        return self._effects

    @tile.setter
    def tile(self, new_tile:TileBaseUI):
        """Set the new tile to display."""
        self.image.fill(GRAY_ACCENT_LIGHT)
        self._tile = new_tile
        self._tilenametextbox.text = new_tile.get_display_name() if new_tile else ""
        self._tiledesctextbox.text = new_tile.get_display_description() if new_tile else ""
        self._tiledescpos = add(self._tilenamepos, (0, self._tilenametextbox.image.get_height()+1))
        self._effectdisplay.position = add(
            self._tiledescpos,
            (0, self._tiledesctextbox.image.get_height()+3)
        )
        self.update(0)
        self._draw_effect_separator()

    @effects.setter
    def effects(self, new_effects:"list[EffectBaseUI]"):
        """Set the new effects to display."""
        self._effects = new_effects
        self._effectdisplay.set_effects(new_effects)
        self.update(0)
        self._draw_effect_separator()

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from Widget.get_blits(self)
        yield from self._sub_blits
        yield from self._effectdisplay.get_blits()

    #pylint: disable=missing-function-docstring
    def update(self, delta_time:float):
        self.image.blit(self._tilenametextbox.image, self._tilenamepos)
        self.image.blit(self._tiledesctextbox.image, self._tiledescpos)
        self.image.fill(IMAGE_BACKGROUND, (*self._imagepos,*STANDARD_TILE_SIZE))
        self._sub_blits.clear()
        if self._tile:
            tile_rect = pygame.Rect(self._imagepos, STANDARD_TILE_SIZE)
            self.image.blits([(blit[0], tile_rect , blit[2]) for blit in self._tile.get_blits()])
            for effect in self._effects:
                self.image.blits([(blit[0], tile_rect, blit[2]) for blit in effect.get_blits()])

    def _draw_border(self):
        pygame.draw.rect(
            self.image,
            GRAY_ACCENT_DARK,
            (
                0,0,
                TileDisplay.IMAGE_SIZE_BORDER[0] - HUD.IMAGE_BORDER_WIDTH/2,
                TileDisplay.IMAGE_SIZE_BORDER[1] - HUD.IMAGE_BORDER_WIDTH/2,
            ),
            HUD.IMAGE_BORDER_WIDTH
            )

    def _draw_effect_separator(self):
        start = add(self._effectdisplay.position, (0,-2))
        end = add(start, (TileDisplay.LABEL_SIZE[0]-1,0))
        pygame.draw.line(self.image, WHITE, start, end)


class UnitDisplay(IGraphics):
    """Allows for easier display of a unit on the HUD."""
    IMAGE_SIZE = STANDARD_UNIT_SIZE
    IMAGE_SIZE_BORDER = (
        2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[0],
        2*HUD.IMAGE_BORDER_WIDTH + IMAGE_SIZE[1]
    )
    SIZE = (200, IMAGE_SIZE_BORDER[1]+20)
    LABEL_SIZE = (SIZE[0] - IMAGE_SIZE_BORDER[0], HUD.LABEL_HEIGHT)

    def __init__(self):
        super().__init__()
        self.imagepos = (
            UnitDisplay.SIZE[0] - UnitDisplay.IMAGE_SIZE[0] - HUD.IMAGE_BORDER_WIDTH,
            HUD.IMAGE_BORDER_WIDTH
        )
        self.titlepos =           (0, UnitDisplay.LABEL_SIZE[1]*0   + 0)
        self.abilityimagepos =    (0, UnitDisplay.LABEL_SIZE[1]*1   + 1)
        self.abilityphasepos =    (0, UnitDisplay.LABEL_SIZE[1]*2   + 2)
        self.abilitycooldownpos = (0, UnitDisplay.LABEL_SIZE[1]*2.5 + 4)
        self.statuseffectpos =    (0, UnitDisplay.LABEL_SIZE[1]*3   + 4)
        self.defaultimagecolor =   (30,  0,  0, 255)
        self.defaulttextboxcolor = (50, 50, 50, 255)
        self.font =                pygame.font.Font('HighOne.ttf', HUD.TITLE_FONT_SIZE)
        self.ability_number_font = pygame.font.Font('HighOne.ttf', HUD.DESC_FONT_SIZE )
        self.cooldown_font =       pygame.font.Font('HighOne.ttf', HUD.SMALL_FONT_SIZE)
        self.image = pygame.Surface(UnitDisplay.SIZE).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0))
        self.displayunit:"UnitBase" = None
        self.displayunitui:"UnitBaseUI" = None
        self.set_displayunit(None)
        self._draw_border()

    def set_displayunit(self, unit_ui:"UnitBaseUI|None"):
        """Set the new unit to display."""
        self._draw_layout()
        self.displayunitui = unit_ui
        self.displayunit = unit_ui._parentelement if unit_ui else None
        if self.displayunit:
            title_text = self.font.render(unit_ui.get_display_name(), True, (255,255,255,255))
            self.image.blit(
                title_text,
                add(self.titlepos, (0, (self.LABEL_SIZE[1]-title_text.get_height())/2))
            )
            for blit in unit_ui.get_blits():
                self.image.blit(blit[0], pygame.Rect(self.imagepos, STANDARD_UNIT_SIZE) , blit[2])
            self.display_abilities()
            self.display_statuseffects()

    #pylint: disable=missing-function-docstring
    def update(self, delta_time:float):
        self.image.fill(self.defaultimagecolor, (*self.imagepos, *STANDARD_UNIT_SIZE))
        if self.displayunit:
            tfc = self.displayunitui.get_component(TransformComponent)
            if tfc:
                unit_pos = tfc.get_position()
                for surface, pos, size in self.displayunitui.get_blits():
                    pos = pygame.Rect(
                        add(sub(pos.topleft, unit_pos), self.imagepos),
                        STANDARD_UNIT_SIZE
                    )
                    self.image.blit(surface, pos, size)

    def display_statuseffects(self):
        self.image.fill((0), (0,100,200,16))
        for i,statuseffect in enumerate(self.displayunit.statuseffects):
            texkey = statuseffect.name
            spritesheet = Textures.get_spritesheet(texkey)
            if spritesheet:
                self.image.blit(spritesheet[0], (1+i*16, self.statuseffectpos[1]+1))
            else:
                log(f"HUD: Texture {texkey} not found.")
                self.image.fill((255,0,255), (1+i*16,self.statuseffectpos[1]+1,16,16))

    def display_abilities(self):
        """Display the abilities of a unit."""
        abilities = self.displayunit.ability_component._abilities
        index = 0
        for ability in abilities:
            if type(ability).__name__ in Textures.abilitytexturemapping.values():
                abilityimage = Textures.get_spritesheet(type(ability).__name__)[0]
                self.image.blit(abilityimage, add(self.abilityimagepos, (17*index, 2)), (0,0,16,16))
            else:
                log(f"HUD: Texture {type(ability).__name__} not found.", 2)

            self.image.fill(PHASECOLORS[ability.phase],
                (*add(self.abilityphasepos, (17*index, 0)), 16, 12)
            )
            if self.displayunit:
                text = str(index+1)
                ability_number_image = self.ability_number_font.render(text, True, WHITE)
                ability_number_pos = add(
                    self.abilityphasepos,
                    (17*(index+1)-ability_number_image.get_width()-2, -1)
                )
                self.image.blit(ability_number_image, ability_number_pos)

            if ability.primed and ability.remainingcooldown == 0:
                col = (100,150,100,255)
            elif ability.remainingcooldown == 0:
                col = (150,150,150,255)
            else:
                col = (150,100,100,255)
            self.image.fill(col, (*add(self.abilitycooldownpos, (17*index, 0)), 16, 8))
            if self.displayunit:
                text = str(ability.remainingcooldown)
                cooldown_number_image = self.cooldown_font.render(text, True, GRAY_ACCENT_DARK)
                cooldown_number_pos = add(
                    self.abilitycooldownpos,
                    (17*(index+1)-cooldown_number_image.get_width()-2, -1)
                )
                self.image.blit(cooldown_number_image, cooldown_number_pos)
            index += 1

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield (self.image, self.rect, self.image.get_rect())

    def _draw_border(self):
        pygame.draw.rect(
            self.image,
            GRAY_ACCENT_LIGHT,
            (
                UnitDisplay.SIZE[0] - UnitDisplay.IMAGE_SIZE_BORDER[0],
                0,
                UnitDisplay.IMAGE_SIZE_BORDER[0] - HUD.IMAGE_BORDER_WIDTH/2,
                UnitDisplay.IMAGE_SIZE_BORDER[1] - HUD.IMAGE_BORDER_WIDTH/2,
            ),
            HUD.IMAGE_BORDER_WIDTH)

    def _draw_layout(self):
        self.image.fill(self.defaultimagecolor,   (*self.imagepos, *STANDARD_UNIT_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.titlepos,        *UnitDisplay.LABEL_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.abilityimagepos, *UnitDisplay.LABEL_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.abilityphasepos, *UnitDisplay.LABEL_SIZE))
        self.image.fill(self.defaulttextboxcolor, (*self.statuseffectpos, *UnitDisplay.LABEL_SIZE))
        pygame.draw.line(
            self.image, GRAY_ACCENT_LIGHT, add(self.abilityimagepos,(0,-1)),
            add(self.abilityimagepos,(UnitDisplay.LABEL_SIZE[0],-1)))
        pygame.draw.line(
            self.image, GRAY_ACCENT_LIGHT, add(self.abilityphasepos,(0,-1)),
            add(self.abilityphasepos,(UnitDisplay.LABEL_SIZE[0],-1)))
        pygame.draw.line(
            self.image, BLACK, add(self.statuseffectpos, (0,-2)),
            add(self.statuseffectpos,(UnitDisplay.LABEL_SIZE[0],-2)), 2)


class EffectInfoGroup(Widget, InputAcceptor):
    """Displays World Effects."""
    def __init__(self, width: int) -> None:
        Widget.__init__(self)
        InputAcceptor.__init__(self)

        self.effects:"list[EffectBaseUI]" = []
        self.effect_icons = HorizontalLayoutSurface()
        self.effect_icons.parent = self

        self._marker_size = (16,16)
        self.selection_marker = pygame.Surface(self._marker_size).convert_alpha()
        self.selection_marker.fill((0))
        pygame.draw.rect(self.selection_marker, WHITE, (0,0,*self._marker_size), 1)

        self.selection_index = 0

        self.title_tb = TextBox("", fontsize=16, bgcolor=(50,50,50), linewidth=width)
        self.title_tb.position = (0,18)
        self.title_tb.parent = self

        self.desc_tb = TextBox("", fontsize=16, bgcolor=(50,50,50), linewidth=width)
        self.desc_tb.parent = self.title_tb

    #pylint: disable=missing-function-docstring
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self.effect_icons.get_blits()
        if self.selection_index in range(len(self.effect_icons.children)):
            yield (self.selection_marker,
                pygame.Rect(
                    self.effect_icons.get_screen_child_pos(self.selection_index),
                    self._marker_size
                ),
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

    def set_effects(self, effects:"list[EffectBaseUI]") -> None:
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


class AbilityDisplay(IGraphics):
    def __init__(self) -> None:
        super().__init__()
        self._abilityuis: "list[AbilityBaseUI]" = []
        self._anims: "list[Animation]" = []
        
    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        for animation in self._abilityuis:
            yield from animation.get_blits()
        for animation in self._anims:
            yield from animation.get_blits()

    def update(self, delta_time:float):
        for animation in self._abilityuis:
            animation.tick(delta_time)
            if not animation.playing:
                self._abilityuis.remove(animation)
        for animation in self._anims:
            animation.tick(delta_time)
            if not animation._running:
                self._anims.remove(animation)

    def play_simple_anim(self, animation:"AbilityBaseUI"):
        self._anims.append(animation)

    def play_ability_anim(self, animation:"AbilityBaseUI"):
        self._abilityuis.append(animation)
