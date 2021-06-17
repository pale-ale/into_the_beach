from hashlib import new
from EPhases import PHASES
import random

class AbilityBase:
    def __init__(self, unit):
        self._unit = unit
        self.needstarget = False
        self.area_of_effect = set()
        self.selected_targets = list()
        self.id = -1
        self.phase = 2
        self.register_hooks()
    
    def activate(self):
        print("Activated", type(self).__name__)
    
    def targets_chosen(self, targets):
        print("Targets chosen for " + type(self).__name__ + ":", targets)

    def register_hooks(self):
        self._unit.register_hook("OnUpdatePhase", self.on_update_phase)
    
    def on_update_phase(self, newphase):
        if newphase == self.phase:
            self.activate()
    

class MovementAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)
        self.id = 0
        self.phase = 3
        #contains all the tilepositions the bound unit could move to
    
    def register_hooks(self):
        super().register_hooks()
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
        assert isinstance(targets, list) and len(targets) == 1
        target = targets[0]
        if target in self.area_of_effect:
            self.selected_targets = [target]
            
    def activate(self):
        super().activate()
        fromxy = self._unit.get_position()
        if len(self.selected_targets) > 0:
            self._unit.grid.move_unit(*fromxy, *self.selected_targets[0])


class PunchAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)
        self.id = 1
        self.phase = 2
    
    def on_update_phase(self, newphase):
        super().on_update_phase(newphase)

    def register_hooks(self):
        super().register_hooks()
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
            self.selected_targets = [target]
            
    def activate(self):
        super().activate()
        if len(self.selected_targets) > 0:
            self._unit.attack(self.selected_targets[0], 10)
            self.area_of_effect.clear()

    
class RangedAttackAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)
        self.id = 2
        self.phase = 2

    def register_hooks(self):
        super().register_hooks()
        self._unit.register_hook("UserAction", self.collect_target_info)
        self._unit.register_hook("OnDeselect", lambda: self.area_of_effect.clear())
    
    def get_ordinals(self):
        x,y = self._unit.get_position()
        width = self._unit.grid.width
        height = self._unit.grid.height
        ordinals = set()
        for i in range (width):
            ordinals.add((i,y))
        for i in range (height):
            ordinals.add((x,i))
        ordinals.remove((x,y))
        return ordinals

    def collect_target_info(self):
        pos = self._unit.get_position()
        self.area_of_effect = self.get_ordinals()
        self.area_of_effect = self.area_of_effect.difference(self._unit.grid.get_ordinal_neighbors(*pos))
        self._unit.register_hook("TargetSelected", self.targets_chosen)

    def targets_chosen(self, targets):
        assert len(targets) == 1
        target = targets[0]
        if target in self.area_of_effect:
            self.selected_targets = [target]
            self.area_of_effect.clear()

    def activate(self):
        super().activate()
        if len(self.selected_targets) > 0:
            self._unit.attack(self.selected_targets[0], 10)
    

class PushAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)
        self.id = 3

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
        unitposx, unitposy = self._unit.get_position()
        newpos = [2*target[0]-unitposx, 2*target[1]-unitposy]
        if target in self.area_of_effect:
            if not self._unit.grid.is_coord_in_bounds(*newpos) or \
            self._unit.grid.is_space_empty(True ,*newpos):
                pass # unit falls from grid
            else:
                if self._unit.grid.is_space_empty(False ,*newpos):
                    self._unit.grid.move_unit(*target, *newpos)
                else:
                    pass # units collide
        self.area_of_effect.clear()
