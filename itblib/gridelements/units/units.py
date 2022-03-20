from itblib.abilities.base_abilities.ranged_abliity_base import \
    RangedAbilityBase
from itblib.abilities.burrow_ability import BurrowAbility
from itblib.abilities.dreadful_noise_ability import DreadfulNoiseAbility
from itblib.abilities.heal_ability import HealAbility
from itblib.abilities.movement_ability import MovementAbility
from itblib.abilities.objective_ability import ObjectiveAbility
from itblib.abilities.punch_ability import PunchAbility
from itblib.abilities.push_ability import PushAbility
from itblib.abilities.serrate_ability import SerrateAbility
from itblib.globals.Enums import EFFECT_IDS, PHASES
from itblib.gridelements.world_effects import EffectStartingArea
from itblib.gridelements.units.UnitBase import UnitBase


class UnitSaucer(UnitBase):
    """A ranged unit with high movement and mobility."""
    def __init__(self, grid, pos, ownerid, name:str="Saucer"):
        super().__init__(grid, pos, ownerid, name=name, 
            abilities=[
                MovementAbility,
                RangedAbilityBase,
                PushAbility
            ]
        )


class UnitBloodWraith(UnitBase):
    """Can apply bleeding, heals when it kills others."""
    def __init__(self, grid, pos, ownerid, name:str="BloodWraith"):
        super().__init__(grid, pos, ownerid, name=name,
            abilities=[HealAbility, MovementAbility, SerrateAbility]
        )

    #pylint: disable=missing-function-docstring
    def attack(self, target:"tuple[int,int]" , damage:int, damagetype:str):
        unit = self.grid.get_unit(target)
        if unit:
            killingblow = unit._hitpoints > 0
            super().attack(target, damage, damagetype)
            if unit._hitpoints <= 0 and killingblow:
                self.change_hp(1,"physical")


class UnitHomebase(UnitBase):
    """The objective of the standard game mode. If it dies, the player loses."""
    def __init__(self, grid, pos, ownerid, name:str="Homebase"):
        super().__init__(grid, pos, ownerid, name=name, abilities=[ObjectiveAbility])

    #pylint: disable=missing-function-docstring
    def on_update_phase(self, new_phase: int):
        super().on_update_phase(new_phase)
        if new_phase == PHASES.PREGAMEPHASE:
            for neighbor in self.grid.get_neighbors(self.pos, ordinal=True, cardinal=True):
                effect:EffectStartingArea = self.grid.add_worldeffect(
                    neighbor, EFFECT_IDS.index("StartingArea")
                )
                if effect:
                    effect.ownerid = self.ownerid


class UnitKnight(UnitBase):
    """A simple brawler."""
    def __init__(self, grid, pos, ownerid, name:str="Knight"):
        super().__init__(grid, pos, ownerid, name=name,
            abilities=[MovementAbility, PunchAbility]
        )


class UnitBurrower(UnitBase):
    """A defensive unit which can resist pushes while burrowed."""
    def __init__(self, grid, pos, ownerid, name:str="Burrower"):
        super().__init__(grid, pos, ownerid, name=name,
            abilities=[BurrowAbility, MovementAbility, PunchAbility]
        )


class UnitSirenHead(UnitBase):
    """A ranged unit that can weaken opponents in its AOE."""
    def __init__(self, grid, pos, ownerid, name:str="SirenHead"):
        super().__init__(grid, pos, ownerid, name=name,
            abilities=[MovementAbility, PunchAbility, DreadfulNoiseAbility]
        )


class UnitChipmonk(UnitBase):
    """A simple, fragile healer"""
    def __init__(self, grid, pos, ownerid, name:str="Chipmonk"):
        super().__init__(grid, pos, ownerid, name=name, hitpoints=3,
            abilities=[MovementAbility, HealAbility]
        )
