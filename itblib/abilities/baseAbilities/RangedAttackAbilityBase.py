from itblib.abilities.baseAbilities.AbilityBase import AbilityBase
from itblib.components.AbilityComponent import AbilityComponent
from itblib.globals.Enums import PREVIEWS


class RangedAttackAbility(AbilityBase):
    """A simple ranged attack, with a targeting scheme like the artillery in ITB."""

    def __init__(self, owning_component:"AbilityComponent"):
        super().__init__(owning_component=owning_component, phase=2, cooldown=2)
    
    def on_select_ability(self):
        super().on_select_ability()
        for coord in self._get_valid_targets():
            self.area_of_effect.add((coord, PREVIEWS[0]))

    def set_targets(self, targets:"list[tuple[int,int]]"):
        assert len(targets) == 1, f"Invalid targets: {targets}"
        super().set_targets(targets)
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions:
            self.selected_targets = [target]
            self.area_of_effect.clear()
  
    def on_trigger(self):
        super().on_trigger()
        owner = self.get_owner()
        if owner and len(self.selected_targets) > 0:
            damage = [owner.baseattack["physical"], "physical"]
            self.get_owner().attack(self.selected_targets[0], *damage)
    
    def confirm_target(self, target: "tuple[int,int]", primed=True):
        if self._is_valid_target(target):
            self.selected_targets = [target]
            super().confirm_target(target, primed=primed)
            self.area_of_effect = {(target, PREVIEWS[-1])}
    
    def _get_valid_targets(self) -> "set[tuple[int,int]]":
        owner = self.get_owner()
        if owner:
            pos = owner.pos
            coords = self._get_ordinals(pos, owner.grid.size)
            coords = coords.difference(owner.grid.get_neighbors(pos))
        return coords
    
    def _get_ordinals(self, origin:"tuple[int,int]", dimensions:"tuple[int,int]"):
        x,y = origin
        ordinals:"set[tuple[int,int]]" = set()
        for i in range (dimensions[0]):
            ordinals.add((i,y))
        for i in range (dimensions[1]):
            ordinals.add((x,i))
        ordinals.remove((x,y))
        return ordinals
   