from itblib.abilities.baseAbilities.ConeAttackAbilityBase import \
    ConeAttackAbilityBase
from itblib.gridelements.StatusEffects import StatusEffectDreadfulNoise


class DreadfulNoiseAbility(ConeAttackAbilityBase):
    """A cone-targeted ability, weakening opponents and friendlies alike."""

    def apply_to_target(self, target: "tuple[int,int]"):
        owner = self.get_owner()
        targetunit = owner.grid.get_unit(target)
        if targetunit and targetunit != owner:
            dreadfulnoiseeffect = StatusEffectDreadfulNoise(targetunit)
            targetunit.add_status_effect(dreadfulnoiseeffect)
