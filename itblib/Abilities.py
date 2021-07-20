from itblib.Enums import PREVIEWS
from itblib.net.NetEvents import NetEvents
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itblib.gridelements.Units import UnitBase

class AbilityBase:
    """
    The base class for all the other abilities.
    Abilities are used to provide unique actions to units.
    They usually come with an active phase during which they are proc'd,
    a cost, cooldowns and other mechanics.
    """

    def __init__(self, unit:"UnitBase"):
        self._unit = unit
        self.needstarget = False
        self.area_of_effect:"list[tuple[tuple[int,int],int]]" = []
        self.selected_targets:"list[tuple[int,int]]" = []
        self.selected = False
        self.id = -1
        self.phase = -1
    
    def tick(self, dt:float):
        """Made to be overridden."""
        pass
    
    def activate(self):
        """Called when an ability gets proc'd."""
        print("Activated", type(self).__name__)
    
    def on_select_ability(self):
        """Called when a player wants to use this ability."""
        if not self.selected:
            self.selected = True
            print("Selected", type(self).__name__)
    
    def on_deselect_ability(self):
        """Called when the ability is not selected any longer, e.g. by selecting a different one."""
        if self.selected:
            self.selected = False
            self.area_of_effect.clear()
            print("Deselected", type(self).__name__)
    
    def on_parentunit_select(self):
        """Called when the unit has been selected (not as a target)."""
        print("My parent was selected.")
    
    def on_parentunit_deselect(self):
        """Called when the unit was deselected (not as a target)."""
        print("My parent was deselected.")
        self.on_deselect_ability()
    
    def on_targets_chosen(self, targets):
        """Called when a player selects a target with enter."""
        if self.selected:
            print("Targets chosen for " + type(self).__name__ + ":", targets)
    
    def on_update_cursor(self, newcursorpos):
        """Called when the player changes the cursor's position while this ability is active."""
        if self.selected:
            print("User moved cursor to", newcursorpos)

    def on_update_phase(self, newphase:int):
        """Called when a phase change occured. Not necessarily a new phase."""
        if newphase == self.phase:
            self.activate()
    
    def on_death(self):
        """Called when this ability's unit dies."""
        print("This uni has died.")

class MovementAbility(AbilityBase):
    """
    Allows units to move around on the map. 
    
    Comes with a movement range and other mechanics, like being able to fly to pass over certain terrain,
    phase through walls and enemies etc.
    """

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
        """Gather the tiles we can move to and add them to the displayed AOE."""
        pathwithself = [self._unit.pos] + self.path
        if len(pathwithself) <= self._unit.moverange:
            pos = pathwithself[-1]
            for neighbor in self._unit.grid.get_ordinal_neighbors(*pos):
                delta = (neighbor[0] - pos[0], neighbor[1] - pos[1])
                coordwithpreviewid = (neighbor, PREVIEWS[delta])
                self.area_of_effect.append(coordwithpreviewid)

    def on_targets_chosen(self, targets:"list[tuple[int,int]]"):
        """Handle the user's target selection."""
        super().on_targets_chosen(targets)
        if len(self.path) > self._unit.moverange:
            return
        assert isinstance(targets, list) and len(targets) == 1
        assert isinstance(targets[0], tuple)
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions:
            pathwithself = [self._unit.pos] + self.path
            pos = pathwithself[-1]
            if target != pos:
                self.add_to_movement(target)
                NetEvents.snd_netunitmove(self._unit)
                self.collect_movement_info()
        self.on_deselect_ability()
    
    def update_path_display(self):
        """Display the new path using proximity textures."""
        self.selected_targets.clear()
        self.area_of_effect.clear()
        pathwithself = [self._unit.pos] + self.path
        if len(pathwithself) > 1:
            first = (pathwithself[0], PREVIEWS[1])
            last = (pathwithself[-1], PREVIEWS[1])
            for i in range(1, len(pathwithself)-1):
                prev = pathwithself[i-1]
                curr = pathwithself[i]
                next = pathwithself[i+1]
                prevdelta = (curr[0] - prev[0], curr[1] - prev[1])
                nextdelta = (next[0] - curr[0], next[1] - curr[1])
                currentwithpreview = (curr, PREVIEWS[(*nextdelta, *prevdelta)])
                self.selected_targets.append(curr)
                self.area_of_effect.append(currentwithpreview)
            self.area_of_effect.append(first)
            self.area_of_effect.append(last)
            self.selected_targets.append(first[0])
            self.selected_targets.append(last[0])
        self.collect_movement_info()

    def add_to_movement(self, target:"tuple[int,int]"):
        """Add a "step" to the path we want to take."""
        self.path.append(target)
        NetEvents.snd_netunitmovepreview(self._unit)
        self.update_path_display()

    def set_path(self, newpath: "list[tuple[int,int]]"):
        """Set the unit's path to newpath."""
        self.path = newpath
        self.update_path_display()
            
    def on_update_cursor(self, newcursorpos:"tuple[int,int]"):
        """Add the new cursor position to the path if we can move there."""
        super().on_update_cursor(newcursorpos)
        if self.selected:
            if len(self.path) < self._unit.moverange:
                self.add_to_movement(newcursorpos)
    
    def activate(self):
        """Set the unit as "active", meaning the phase will not continue until it has finished moving."""
        super().activate()
        self.area_of_effect.clear()
        self.timinginfo = self._unit.age
        self._unit.done = False


class PunchAbility(AbilityBase):
    """A simple damaging ability. Deals damage to a neighboring target."""

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit)
        self.id = 1
        self.phase = 2

    def on_select_ability(self):
        super().on_select_ability()
        pos = self._unit.pos
        for neighbor in self._unit.grid.get_ordinal_neighbors(*pos):
            self.area_of_effect.append((neighbor, PREVIEWS[0]))

    def on_targets_chosen(self, targets:"list[tuple[int,int]]"):
        super().on_targets_chosen(targets)
        assert len(targets) == 1
        target = targets[0]
        positions = [x[0] for x in self.area_of_effect]
        if target in positions:
            self.selected_targets = [target]
            self.area_of_effect.clear()
            self.on_deselect_ability()
            
    def activate(self):
        super().activate()
        if len(self.selected_targets) > 0:
            damage = [self._unit.baseattack["physical"], "physical"]
            self._unit.attack(self.selected_targets[0], *damage)
            self.area_of_effect.clear()
            self.selected_targets.clear()

    
class RangedAttackAbility(AbilityBase):
    """A simple ranged attack, with a targeting scheme like the artillery in ITB."""

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit)
        self.id = 2
        self.phase = 2

    def get_ordinals(self):
        x,y = self._unit.pos
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
        pos = self._unit.pos
        coords = self.get_ordinals()
        coords = coords.difference(self._unit.grid.get_ordinal_neighbors(*pos))
        #for coord in coords:
        #    self.area_of_effect.append(coord)

    def on_targets_chosen(self, targets:"list[tuple[int,int]]"):
        super().on_targets_chosen(targets)
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
    """A melee attack pushing a target away from the attacker."""

    def __init__(self, unit:"UnitBase"):
        super().__init__(unit)
        self.id = 3
        self.phase = 2

    def on_targets_chosen(self, targets:"list[tuple[int,int]]"):
        super().on_targets_chosen(targets)
        assert len(targets) == 1
        positions = [x[0] for x in self.area_of_effect]
        target = targets[0]
        if target in positions:
            self.selected_targets = [target]
        self.area_of_effect.clear()

    def on_select_ability(self):
        super().on_select_ability()
        pos = self._unit.pos
        for neighbor in self._unit.grid.get_ordinal_neighbors(*pos):
            self.area_of_effect.append((neighbor, PREVIEWS[0]))

    def activate(self):
        super().activate()
        if len(self.selected_targets):
            unitposx, unitposy = self._unit.pos
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
    """This ability makes a unit an "Objective", meaning the player loses if it dies."""
    def __init__(self, unit:"UnitBase"):
            super().__init__(unit)
            self.id = 4

    def on_death(self):
        super().on_death()
        print("I lost..")
