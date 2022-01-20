from typing import TYPE_CHECKING

import pygame

from itblib.abilities.TargetAbilityBase import TargetAbilityBase
from itblib.globals.Enums import PREVIEWS

if TYPE_CHECKING:
    from itblib.gridelements.units.UnitBase import UnitBase

class DreadfulNoiseAbility(TargetAbilityBase):
    """A cone-targeted ability, weakening opponents and friendlies alike."""

    def __init__(self, unit:"UnitBase"):
        self.cone_angle = 0
        super().__init__(unit, 3, 5)

    def on_select_ability(self):
        super().on_select_ability()
        for neighbor in self._get_valid_targets():
            self.area_of_effect.add((neighbor, PREVIEWS[0]))

    def apply_to_target(self, target: "tuple[int,int]"):
        super().apply_to_target(target)
        owner = self.get_owner()
        damage = [owner.baseattack["physical"], "physical"]
        owner.attack(self.selected_targets[0], *damage)
    
    def handle_key_event(self, event: any) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.cone_angle += .1
                return True
            if event.key == pygame.K_RIGHT:
                self.cone_angle += .1
                return True
        return super().handle_key_event(event)

    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        owner = self.get_owner()
        return owner.grid.get_neighbors(owner.pos, ordinal=True, cardinal=True)
