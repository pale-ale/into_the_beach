from Enums import PREVIEWS

class AbilityBase:
    def __init__(self, unit):
        self._unit = unit
        self.needstarget = False
        self.area_of_effect = set()
        self.selected_targets = list()
        self.id = -1
        self.phase = 2
        self.register_hooks()
    
    def tick(self, dt):
        pass

    def on_select_ability(self):
        print("Selected", type(self).__name__)
    
    def on_deselect_abilities(self):
        print("Deselected", type(self).__name__)
    
    def activate(self):
        print("Activated", type(self).__name__)
    
    def targets_chosen(self, targets):
        print("Targets chosen for " + type(self).__name__ + ":", targets)

    def register_hooks(self):
        self._unit.register_hook("UserAction", self.on_select_ability)
        self._unit.register_hook("TargetSelected", self.targets_chosen)
        self._unit.register_hook("OnDeselectAbilities", self.on_deselect_abilities)
        self._unit.register_hook("OnDeselectUnit", self.on_deselect_abilities)
        self._unit.register_hook("OnUpdatePhase", self.on_update_phase)
    
    def on_update_phase(self, newphase):
        if newphase == self.phase:
            self.activate()
    

class MovementAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)
        self.id = 0
        self.phase = 3
        self.timinginfo = unit.age
        self.durationperstep = .5 #seconds
        self.path = []
    
    def on_deselect_abilities(self):
        super().on_deselect_abilities()
        self.area_of_effect.clear()
    
    def on_select_ability(self):
        super().on_select_ability()
        self.path.clear()
        self.area_of_effect.clear()
        self.selected_targets.clear()
        self.collect_movement_info()

    def collect_movement_info(self):
        self.area_of_effect = set()
        pathwithself = [self._unit.get_position()] + self.path
        if len(self.path) <= self._unit.moverange:
            pos = self._unit.get_position()
            for neighbor in self._unit.grid.get_ordinal_neighbors(*pathwithself[-1]):
                delta = (neighbor[0] - pos[0], neighbor[1] - pos[1])
                coordwithpreviewid = (neighbor, PREVIEWS[delta])
                self.area_of_effect.add(coordwithpreviewid)

    def targets_chosen(self, targets):
        assert isinstance(targets, list) and len(targets) == 1
        target = targets[0]
        if target in self.area_of_effect:
            if target not in self.path:
                self.path.append(target)
                self.area_of_effect.add(target)
                self.selected_targets.append(target)
                print("adding target")
        self.collect_movement_info()
    
    def tick(self, dt):
        if not self._unit.done and self.timinginfo + self.durationperstep <= self._unit.age:
            fromxy = self._unit.get_position()
            if len(self.selected_targets) > 0:
                self._unit.grid.move_unit(*fromxy, *self.selected_targets[0])
                self.selected_targets.pop(0)
                self.timinginfo += self.durationperstep
            else:
                self._unit.done = True

    def activate(self):
        super().activate()
        self.area_of_effect.clear()
        self.timinginfo = self._unit.age
        self._unit.done = False


class PunchAbility(AbilityBase):
    def __init__(self, unit):
        super().__init__(unit)
        self.id = 1
        self.phase = 2
    
    def on_deselect_abilities(self):
        super().on_deselect_abilities()
        self.area_of_effect.clear()

    def on_select_ability(self):
        super().on_select_ability()
        pos = self._unit.get_position()
        self.area_of_effect = self._unit.grid.get_ordinal_neighbors(*pos)
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
            damage = [self._unit.baseattack["physical"], "physical"]
            self._unit.attack(self.selected_targets[0], *damage)
            self.area_of_effect.clear()
            self.selected_targets.clear()

    
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
            damage = [self._unit.baseattack["physical"], "physical"]
            self._unit.attack(self.selected_targets[0], *damage)
    

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
                    targetint = self._unit.grid.c_to_i(target)
                    self._unit.grid.units(targetint).on_take_damage(1, "collosion")
                    newposint = self._unit.grid.c_to_i(newpos)
                    self._unit.grid.units(newposint).on_take_damage(1, "collosion")
        self.area_of_effect.clear()
