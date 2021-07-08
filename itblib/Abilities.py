from typing import TYPE_CHECKING
from .Enums import PREVIEWS
from .net import NetEvents

if TYPE_CHECKING:
    from itblib.gridelements.Units import UnitBase

class AbilityBase:
    def __init__(self, unit:"UnitBase"):
        self._unit = unit
        self.needstarget = False
        self.area_of_effect:"list[tuple[tuple[int,int],int]]" = []
        self.selected_targets:"list[tuple[tuple[int,int],int]]" = []
        self.selected = False
        self.id = -1
        self.phase = 2
        self.register_hooks()
    
    def tick(self, dt:float):
        pass

    def on_select_ability(self):
        if not self.selected:
            self.selected = True
            print("Selected", type(self).__name__)
    
    def on_deselect_abilities(self):
        if self.selected:
            self.selected = False
            self.area_of_effect.clear()
            print("Deselected", type(self).__name__)
    
    def activate(self):
        print("Activated", type(self).__name__)
    
    def targets_chosen(self, targets):
        if self.selected:
            print("Targets chosen for " + type(self).__name__ + ":", targets)
    
    def on_update_cursor(self, newcursorpos):
        if self.selected:
            print("User moved cursor to", newcursorpos)

    def register_hooks(self):
        self._unit.register_hook("UserAction", self.on_select_ability)
        self._unit.register_hook("TargetSelected", self.targets_chosen)
        self._unit.register_hook("OnDeselectAbilities", self.on_deselect_abilities)
        self._unit.register_hook("OnDeselectUnit", self.on_deselect_abilities)
        self._unit.register_hook("OnUpdatePhase", self.on_update_phase)
        self._unit.register_hook("OnUpdateCursor", self.on_update_cursor)
    
    def on_update_phase(self, newphase:int):
        if newphase == self.phase:
            self.activate()
    

class MovementAbility(AbilityBase):
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit)
        self.id = 0
        self.phase = 3
        self.timinginfo = unit.age
        self.durationperstep = .5 #seconds
        self.path = []
    
    def on_select_ability(self):
        super().on_select_ability()
        if  self.selected:
            self.path.clear()
            self.area_of_effect.clear()
            self.selected_targets.clear()
            self.collect_movement_info()

    def collect_movement_info(self):
        self.area_of_effect = self.selected_targets.copy()
        pathwithself = [self._unit.get_position()] + self.path
        if len(self.path) <= self._unit.moverange:
            pos = pathwithself[-1]
            for neighbor in self._unit.grid.get_ordinal_neighbors(*pathwithself[-1]):
                delta = (neighbor[0] - pos[0], neighbor[1] - pos[1])
                coordwithpreviewid = (neighbor, PREVIEWS[delta])
                self.area_of_effect.append(coordwithpreviewid)

    def targets_chosen(self, targets:"list[tuple[int,int]]"):
        super().targets_chosen(targets)
        if len(self.path) > self._unit.moverange:
            return
        assert isinstance(targets, list) and len(targets) == 1
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions:
            pathwithself = [self._unit.get_position()] + self.path
            pos = pathwithself[-1]
            if target != pathwithself[-1]:
                #SE = 0,1, NE = -1,0
                if len(pathwithself)>1:
                    prevdelta = (pathwithself[-1][0] - pathwithself[-2][0],
                        pathwithself[-1][1] - pathwithself[-2][1])
                    delta = (target[0] - pos[0], target[1] - pos[1], *prevdelta)
                    self.area_of_effect[len(self.path)] = (self.area_of_effect[len(self.path)][0], PREVIEWS[delta])
                    self.selected_targets[-1] = (self.selected_targets[-1][0], PREVIEWS[delta])
                else:
                    prevdelta = (target[0] - pos[0], target[1] - pos[1])
                    delta = (target[0] - pos[0], target[1] - pos[1], *prevdelta)
                self.selected_targets.append((target, PREVIEWS[1]))
                NetEvents.snd_netunitmove(self._unit)
                self.path.append(target)
                self.area_of_effect.append((target, PREVIEWS[1]))
                self.collect_movement_info()
    
    def on_update_cursor(self, newcursorpos:"tuple[int,int]"):
        super().on_update_cursor(newcursorpos)
        if self.selected:
            self.targets_chosen([newcursorpos])
    
    def activate(self):
        super().activate()
        self.area_of_effect.clear()
        self.timinginfo = self._unit.age
        self._unit.done = False


class PunchAbility(AbilityBase):
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit)
        self.id = 1
        self.phase = 2

    def on_select_ability(self):
        super().on_select_ability()
        pos = self._unit.get_position()
        for neighbor in self._unit.grid.get_ordinal_neighbors(*pos):
            self.area_of_effect.append((neighbor, PREVIEWS[0]))

    def targets_chosen(self, targets:"list[tuple[int,int]]"):
        assert len(targets) == 1
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions:
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
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit)
        self.id = 2
        self.phase = 2

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
        return ordinals#
    

    def on_select_ability(self):
        super().on_select_ability()
        pos = self._unit.get_position()
        coords = self.get_ordinals()
        coords = coords.difference(self._unit.grid.get_ordinal_neighbors(*pos))
        for coord in coords:
            self.area_of_effect.append((coord, PREVIEWS[0]))

    def targets_chosen(self, targets:"list[tuple[int,int]]"):
        super().targets_chosen(targets)
        assert len(targets) == 1
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions:
            self.selected_targets = [target]
            self.area_of_effect.clear()

    def activate(self):
        super().activate()
        if len(self.selected_targets) > 0:
            damage = [self._unit.baseattack["physical"], "physical"]
            self._unit.attack(self.selected_targets[0], *damage)
    

class PushAbility(AbilityBase):
    def __init__(self, unit:"UnitBase"):
        super().__init__(unit)
        self.id = 3

    def targets_chosen(self, targets:"list[tuple[int,int]]"):
        super().targets_chosen(targets)
        assert len(targets) == 1
        positions = [x[0] for x in self.area_of_effect]
        target = targets[0]
        if target in positions:
            self.selected_targets = [target]
        self.area_of_effect.clear()

    def on_select_ability(self):
        super().on_select_ability()
        pos = self._unit.get_position()
        for neighbor in self._unit.grid.get_ordinal_neighbors(*pos):
            self.area_of_effect.append((neighbor, PREVIEWS[0]))

    def activate(self):
        super().activate()
        if len(self.selected_targets):
            unitposx, unitposy = self._unit.get_position()
            target = self.selected_targets[0]
            newpos = [2*target[0]-unitposx, 2*target[1]-unitposy]
            if not self._unit.grid.is_coord_in_bounds(*newpos) or \
            self._unit.grid.is_space_empty(True ,*newpos):
                pass # unit falls from grid
            else:
                if self._unit.grid.is_space_empty(False ,*newpos):
                    self._unit.grid.move_unit(*target, *newpos)
                else:
                    targetint = self._unit.grid.c_to_i(*target)
                    self._unit.grid.units[targetint].on_take_damage(1, "collision")
                    newposint = self._unit.grid.c_to_i(*newpos)
                    self._unit.grid.units[newposint].on_take_damage(1, "collision")
        self.selected_targets.clear()
        self.area_of_effect.clear()

class ObjectiveAbility(AbilityBase):        
    def register_hooks(self):
        self._unit.register_hook("OnDeath", self.on_death)
    
    def on_death(self):
        print("I lost..")
