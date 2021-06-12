from typing import Iterable


class AbilityBase:
    def __init__(self, unit):
        self._unit = unit
        self.register_hooks()
        self.needstarget = False
        self.area_of_effect = set()
    
    def targets_chosen(self, targets):
        print("Please override function targets_chosen in class", type(self).__name__)

    def register_hooks(self):
        print("Please override function register_hooks in class", type(self).__name__)


class MovementAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)
        #contains all the tilepositions the bound unit could move to
    
    def register_hooks(self):
        self._unit.register_hook("UserAction", self.collect_movement_info)
        self._unit.register_hook("OnDeselect", lambda: self.area_of_effect.clear())

    def collect_movement_info(self):     
        self.area_of_effect = set()
        newtiles = {self._unit.get_position()}
        tmpnewtiles = set()
        rangefromstart = 0
        while rangefromstart <= self._unit.moverange:
            self.area_of_effect = self.area_of_effect.union(newtiles)
            while len(newtiles) > 0:
                newtilepos = newtiles.pop()
                self.area_of_effect.add(newtilepos)
                for neighborpos in self._unit.grid.get_ordinal_neighbors(*newtilepos):
                    if neighborpos not in self.area_of_effect:
                        tmpnewtiles.add(neighborpos)
            newtiles = tmpnewtiles.copy()
            tmpnewtiles.clear()
            rangefromstart += 1
        self._unit.register_hook("TargetSelected", self.targets_chosen)
    
    def targets_chosen(self, targets):
        assert len(targets) == 1
        target = targets[0]
        if target in self.area_of_effect:
            fromxy = self._unit.get_position()
            self._unit.grid.move_unit(*fromxy, *target)


class PunchAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)

    def register_hooks(self):
        self._unit.register_hook("UserAction", self.collect_target_info)
        self._unit.register_hook("OnDeselect", lambda: self.area_of_effect.clear())
    
    def collect_target_info(self):
        pos = self._unit.get_position()
        self.area_of_effect = self._unit.grid.get_ordinal_neighbors(*pos)
        self._unit.register_hook("TargetSelected", self.targets_chosen)

    def targets_chosen(self, targets):
        assert len(targets) == 1
        target = targets[0]
        if target in self.area_of_effect:
            self._unit.attack(target, 10)
            self.area_of_effect.clear()