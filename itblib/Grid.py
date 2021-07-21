from itblib.gridelements.GridElement import GridElement
from typing import Optional
from itblib.net.Connector import Connector
from itblib.gridelements.Tiles import TileBase
from .gridelements.Effects import EffectBase
from .gridelements.Units import UnitBase, UnitSaucer
from .Maps import Map

from .Globals import ClassMapping
from .Enums import PHASES
from .ui.IGridObserver import IGridObserver
from itblib.net.NetEvents import NetEvents

import random

class Grid:
    """Manager for Data-Only-Objects like units, tiles, effects, etc."""

    def __init__(self, connector:Connector, observer:Optional[IGridObserver]=None, width:int=10, height:int=10):
        self.height = width
        self.width = height
        self.phasetime = 0
        self.gametime = 0
        self.connector = connector
        self.planningphasetime = 10
        self.pregametime = 10
        self.tiles:"list[Optional[TileBase]]" = [None]*width*height
        self.units:"list[Optional[UnitBase]]" = [None]*width*height
        self.effects:"list[Optional[EffectBase]]" = [None]*width*height
        self.observer = observer
        self.phase = 0

    def update_observer(self, observer:Optional[IGridObserver]):
        """
        Set a new observer, which will receive events for e.g. a spawned unit.

        Useful in event-based scenarios, like loading a grpahical display for the new unit.
        """
        self.observer = observer
    
    def everybody_done(self) -> bool:
        """Check whether every member of the grid has finished it's actions, like moving."""
        for group in (self.units, self.tiles, self.effects):    
            for member in group:
                if member and not member.done:
                    return False
        return True

    def update_unit_movement(self):
        """Move units by one step and handle collisions between them or other obstacles."""
        movingunits:"list[UnitBase]" = []
        obstacles:"list[GridElement]" = []
        #filter units that cannot move
        for unit in self.units:
            if unit:
                movementability = unit.get_movement_ability()
                if not movementability or len(movementability.selected_targets) == 0:
                    obstacles.append(unit.pos)
                    unit.done = True
                else:
                    movingunits.append(unit)
        if len(movingunits) > 0:
            nextpositions = {} #position:[units that want to go here]
            # remove units whose path is already exhausted
            # and add their positions into obstacles
            for unit in movingunits[:]:
                path = unit.get_movement_ability().selected_targets
                if len(path) == 0:
                    movingunits.remove(unit)
                    unit.done = True
                    obstacles.append(unit.pos)
            # add each unit and their next move to the dict
            # and remove first path element
            for unit in movingunits[:]:
                nextpos = unit.get_movement_ability().selected_targets.pop(0)
                if nextpos in obstacles:
                    movingunits.remove(unit)
                    unit.done = True
                    obstacles.append(unit.pos)
                if nextpos in nextpositions.keys():
                    nextpositions[nextpos].append(unit)
                else:
                    nextpositions[nextpos] = [unit]
            # if multiple units are registered for the same tile at
            # the same time, both are stopped and turned into obstacles
            for position in nextpositions.keys():
                units = nextpositions[position]
                if len(units) > 1:
                    for unit in units:
                        if unit in movingunits:
                            movingunits.remove(unit)
                            obstacles.append(unit.pos)
                            unit.done = True
                elif len(units) == 1:
                    self.move_unit(units[0].pos, position)

    def change_phase(self, phase):
        """Set the phase to a certain number."""
        self.phase = phase
        self.phasetime = 0
        for unit in self.units:
            if unit:
                unit.on_update_abilities_phases(self.phase)

    def advance_phase(self):
        """Advance phase cycle by one, starting from the planning phase once the end is reached."""
        maxphase = len(PHASES)-1
        nextphase = (self.phase)%maxphase+1
        print("next phase...")
        self.change_phase(nextphase)

    def load_map(self, map:Map):
        """Load a map, spawning all the required units, tiles, etc.."""
        if self.observer:
            self.observer.on_load_map(map)
        self.width = map.width
        self.height = map.height
        self.tiles = [None]*self.width*self.height
        self.units = [None]*self.width*self.height
        self.effects = [None]*self.width*self.height
        for pos, tileid, effectid, unitid in map.iterate_tiles():
            if tileid:
                self.add_tile(pos, tileid)
            if effectid:
                self.add_effect(pos, effectid)
            if unitid:
                self.add_unit(pos, unitid, -1)

    def add_tile(self, pos:"tuple[int,int]", tileid:int):
        """Add a tile to the grid at given position."""
        tiletype = ClassMapping.tileclassmapping[tileid]
        newtile = tiletype(self, pos)
        self.tiles[self.c_to_i(pos)] = newtile
        if self.observer:
            self.observer.on_add_tile(newtile)

    def add_effect(self, pos:"tuple[int,int]", effectid:id):
        """Add an effect to the grid at given position."""
        effecttype = ClassMapping.effectclassmapping[effectid]       
        neweffect = effecttype(self, pos)
        self.effects[self.c_to_i(pos)] = neweffect
        if self.observer:
            self.observer.on_add_effect(neweffect)

    def request_add_unit(self, x, y, unitid:int, playerid:int):
        NetEvents.snd_netunitspawn(unitid, (x,y), playerid)

    def add_unit(self, pos:"tuple[int,int]", unitid:int, ownerid:int):
        """Add a unit to the grid at given position, owned by ownerid."""
        unitclass = ClassMapping.unitidclassmapping[unitid]
        newunit = unitclass(self, pos, ownerid)
        self.units[self.c_to_i(pos)] = newunit
        if self.observer:
            self.observer.on_add_unit(newunit)

    def remove_unit(self, pos:"tuple[int,int]"):
        """Remove a unit at given position."""
        if self.is_space_empty(False, pos):
            print(f"error try to remove unit at {pos} which does not exist.")
            exit(1)
        self.units[self.c_to_i(pos)] = None
        if self.observer:
            self.observer.on_remove_unit(pos)
    
    def move_unit(self, from_pos:"tuple[int,int]", to_pos:"tuple[int,int]"):
        """Move a unit from (x,y) to (tagretx,targety)."""
        if self.is_space_empty(False, from_pos):
            print(f"error try to move unit at {from_pos} which does not exist.")
            exit(1)    
        if self.is_space_empty(False, to_pos) and not \
                self.is_space_empty(True, to_pos):
            unit = self.get_unit(from_pos)
            self.units[self.c_to_i(from_pos)] = None
            self.units[self.c_to_i(to_pos)] = unit
            unit.pos = to_pos
            NetEvents.snd_netunitmove(from_pos, to_pos)
            self.tiles[self.c_to_i(to_pos)].on_enter(unit)
            if self.observer:
                self.observer.on_move_unit(from_pos, to_pos)

    def get_tile(self, x:int, y:int):
        """Return the tile at (x,y)."""
        return self.tiles[self.width*y+x]
   
    def get_effect(self, x:int, y:int):
        """Return the effect at (x,y)."""
        return self.effects[self.width*y+x]
    
    def get_unit(self, pos:"tuple[int,int]"):
        """Return the unit at (x,y)."""
        return self.units[self.c_to_i(pos)]

    def c_to_i(self, coords:"tuple[int,int]"):
        """Convert xy-coordinates to the corresponding index."""
        return self.width*coords[1] + coords[0]

    def is_coord_in_bounds(self, pos:"tuple[int,int]"):
        """Check whether a coordinate is inside the grid space."""
        return pos[0]>=0 and pos[0]<self.width and pos[1]>=0 and pos[1]<self.height

    def is_space_empty(self, tiles:bool, pos:"tuple[int,int]")->bool:
        """Check whether a tile or a unit is at the given position."""
        return self.is_coord_in_bounds(pos) and \
            not (self.tiles if tiles else self.units)[self.c_to_i(pos)]

    def get_ordinal_neighbors(self, x, y):
        """Returns the coordinates of neighboring tiles when inside bounds."""
        assert isinstance(x, int) and isinstance(y, int)
        up = (x-1,y)
        right = (x,y+1)
        down = (x+1,y)
        left = (x,y-1)
        return [n for n in (up, right, down, left) if self.is_coord_in_bounds(n)]

    def tick(self, dt:float):
        """Ticks the game, updating phases, movement and other things."""
        self.gametime += dt
        for u in self.units:
            if u:
                u.tick(dt)
        for t in self.tiles:
            if t:
                t.tick(dt)
        for e in self.effects:
            if e:
                e.tick(dt)
        self.phasetime += dt
        if self.connector.authority:
            if self.phase == 0:
                    if self.phasetime >= self.pregametime:
                        self.advance_phase()
                        NetEvents.snd_netphasechange(self.phase)
                        self.phasetime = 0.0
            elif self.phase == 1:
                    if self.phasetime >= self.planningphasetime:
                        self.advance_phase()
                        NetEvents.snd_netphasechange(self.phase)
                        self.phasetime = 0.0
            elif self.phase in [2,3,4]:
                if self.everybody_done():
                    self.advance_phase()
                    NetEvents.snd_netphasechange(self.phase)
                else:
                    if self.phasetime >= 0.5:
                        self.phasetime = 0.0
                        self.update_unit_movement()

    def show(self):
        """Print the grid onto the console."""
        text = ""
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[self.width*y+x]
                if tile:
                    text += str(tile.id)
                else:
                    text += " "
            text += "\n"
        print(text)
