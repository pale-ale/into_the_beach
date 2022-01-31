import math
from cmath import pi
from typing import Generator

import pygame
from itblib import Vec
from itblib.abilities.baseAbilities.TargetAbilityBase import TargetAbilityBase
from itblib.components.AbilityComponent import AbilityComponent
from itblib.globals.Enums import EAST, NORTH, PREVIEWS
from itblib.Vec import deg_to_coord, sub, vector_between


class ConeAttackAbilityBase(TargetAbilityBase):
    """A cone-targeted ability."""

    def __init__(self, owning_component:"AbilityComponent"):
        super().__init__(owning_component, 3, 5)
        self.cone_spread_angle = pi/2
        self.cone_direction = 0
        #the radius of the cone in tiles
        self.cone_len_tiles = 2

    def handle_key_event(self, event: any) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                return True
            if event.key == pygame.K_LEFT:
                self.cone_direction += self.cone_spread_angle
                self.cone_direction %= 2*pi
                self.on_select_ability()
                return True
            if event.key == pygame.K_RIGHT:
                self.cone_direction -= self.cone_spread_angle
                self.cone_direction %= 2*pi
                self.on_select_ability()
                return True
        return super().handle_key_event(event)
    
    def on_select_ability(self):
        super().on_select_ability()
        for coord in self._get_valid_targets():
            self.area_of_effect.add((coord, PREVIEWS[0]))
    
    def confirm_target(self, target: "tuple[int,int]"):
        self.set_targets([t for t in self._get_valid_targets() if self._is_valid_target(t)])
        super().confirm_target(target)

    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        m = (EAST, NORTH)
        owner = self.get_owner()
        #use (2,2) for debugging in playground
        pos = owner.pos if owner else (2,2)
        possible_target_poss = ConeAttackAbilityBase._get_circle(pos, self.cone_len_tiles + .5)
        dega = self.cone_direction + self.cone_spread_angle/2
        degb = self.cone_direction - self.cone_spread_angle/2
        a = Vec.transform_vector(m, deg_to_coord(dega))
        b = Vec.transform_vector(m, deg_to_coord(degb))
        angle_target_pos = {p for p in possible_target_poss if vector_between(a,b, sub(p, pos))}
        return angle_target_pos
    
    @staticmethod
    def _get_circle(c:tuple[int,int], r:float) -> "Generator[tuple[int,int]]":
        """
        @c: circle center
        @r: radius
        @return: coordinates of potential tiles whose centers are within euclidean distance
        """
        left = c[0] - int(r)
        right = c[0] + int(r)
        top = c[1] - int(r)
        bot = c[1] + int(r)
        for y in range(top, bot+1):
            for x in range(left, right+1):
                if math.sqrt((c[0]-x)**2 + (c[1]-y)**2) <= r:
                    yield (x,y)
