from typing import TYPE_CHECKING, TypeVar

import pygame
from itblib.Log import log
from itblib.Vec import add, smult
from itblib.globals.Constants import STANDARD_UNIT_SIZE
from itblib.globals.math_helpers import get_parabola_time
from itblib.ui.animations import ProjectileAnimation
from itblib.ui.IGraphics import IGraphics

if TYPE_CHECKING:
    from typing import Generator, Type
    from itblib.abilities.base_abilities.ability_base import AbilityBase
    from itblib.ui.hud.hud import Hud
    from itblib.ui.GridUI import GridUI


class AbilityBaseUI(IGraphics):
    def __init__(self, hud:"Hud", ability:"AbilityBase") -> None:
        super().__init__()
        self._hud = hud
        self._ability:"AbilityBase" = ability
        self.playing = True

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        return super().get_blits()

    def on_update_targets(self):
        """Called when an ability's selected targets change."""

    def on_update_cursor(self):
        """Called when the user moved the cursor."""

    def on_trigger(self):
        """Called when an ability triggers."""

    def tick(self, delta_time:float):
        """Tick the animations etc."""

class AbilityProjectileUI(AbilityBaseUI):
    def __init__(self, gridui: "GridUI", ability: "AbilityBase", start, end, speed) -> None:
        """Start and end in grid coords."""
        super().__init__(gridui, ability)
        self.screen_start = add(gridui.transform_grid_screen(start), smult(.5, STANDARD_UNIT_SIZE))
        self.screen_end   = add(gridui.transform_grid_screen(  end), smult(.5, STANDARD_UNIT_SIZE))
        self.speed = speed
        peak = ((self.screen_start[0] + self.screen_end[0])/2, (self.screen_end[1] + self.screen_start[1])/2 - 65)
        self.time = 0
        para = get_parabola_time(peak, self.screen_start, self.screen_end)
        timescaled_para = lambda time: para(time*speed) 
        self._projectile_anim = ProjectileAnimation(timescaled_para)
        self.playing = False

    def on_trigger(self):
        """Called when an ability triggers."""
        print("i got triggered\n\n")
        self.playing = True
        self._projectile_anim.start()

    def get_blits(self) -> "Generator[tuple[pygame.Surface, pygame.Rect, pygame.Rect]]":
        yield from self._projectile_anim.get_blits()

    def tick(self, delta_time: float):
        self.time += delta_time
        if self.time * self.speed > .5:
            self.playing = False
        if self.playing:
            self._projectile_anim.tick(delta_time)

T = TypeVar('T', bound=AbilityBaseUI)

class AbilityUIBuilder():
    hud:"Hud|None" = None
    gridui:"GridUI|None" = None
    classes = {AbilityProjectileUI}
    @classmethod
    def construct_ability_ui(cls, ability:"AbilityBase", ability_ui_cls:"Type[T]", *other_args) -> "T|None":
        assert cls.hud and cls.gridui, f"{cls.__name__} needs a valid gridui and hud in order to create abilityuis." 
        if ability_ui_cls not in cls.classes:
            log(f"AbilityUIBuilder: Couldn't find class '{ability_ui_cls.__name__}'.", 2)
            return None
        ability_ui:"AbilityBaseUI" = ability_ui_cls(cls.gridui, ability, *other_args)
        if cls.hud:
            cls.hud.abilitydisplay.play_ability_anim(ability_ui)
        ability.observer = ability_ui
        return ability_ui
