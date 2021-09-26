from itblib.Globals.GridElementFactory import GridElementFactory
from itblib.gridelements.GridElement import GridElement
from typing import Optional
from itblib.net.Connector import Connector
from itblib.gridelements.Tiles import TileBase
from .gridelements.Effects import EffectBase
from .gridelements.units.UnitBase import UnitBase
from .Maps import Map
from itblib.Globals.Enums import EFFECT_IDS, PHASES, TILE_IDS, UNIT_IDS
from .ui.IGridObserver import IGridObserver
from itblib.net.NetEvents import NetEvents
from itblib.Serializable import Serializable

class Grid(Serializable):
    """Manager for Data-Only-Objects like units, tiles, effects, etc."""

    def __init__(self, connector:Connector, observer:Optional[IGridObserver]=None, width:int=10, height:int=10):
        super().__init__(["width", "height", "phasetime", "tiles", "units", "worldeffects"])
        self.height = height
        self.width = width
        self.phasetime = 0
        self.gametime = 0
        self.connector = connector
        self.planningphasetime = 10
        self.pregametime = 10
        self.tiles:"list[Optional[TileBase]]" = [None]*width*height
        self.units:"list[Optional[UnitBase]]" = [None]*width*height
        self.worldeffects:"list[list[EffectBase]]" = [[] for i in range(width*height)]
        self.observer = observer
        self.phase = 0
    
    def extract_data(self) -> dict:
        customtiles = [t.extract_data() if t else None for t in self.tiles]
        customunits = [u.extract_data() if u else None for u in self.units]
        customworldeffects = []
        for effectstack in self.worldeffects:
            s = []
            for effect in effectstack:
                s.append(effect.extract_data())
            customworldeffects.append(s)

        return super().extract_data(
            custom_fields={
                "tiles":customtiles, 
                "units":customunits,
                "worldeffects":customworldeffects
            }
        )
    
    def insert_data(self, data):
        # TODO: constructing everything every turn might be a bit much, maybe moving
        # units around is a better way to go performance-wise...
        self.phasetime = data["phasetime"]
        self.width = data["width"]
        self.height = data["height"]
        self.tiles:"list[Optional[TileBase]]" = [None]*self.width*self.height
        self.units:"list[Optional[UnitBase]]" = [None]*self.width*self.height
        self.worldeffects:"list[list[EffectBase]]" = [[] for i in range(self.width*self.height)]
        if self.observer:
            self.observer.on_load_map(None)
        for i in range(len(data["tiles"])):
            tiledata = data["tiles"][i]
            if tiledata:
                tiletype = GridElementFactory.find_tile_class(tiledata["name"])
                if tiletype:
                    self.add_tile(
                        self.i_to_c(i), 
                        TILE_IDS.index(tiledata["name"])
                    )
        for i in range(len(data["units"])):
            unitdata = data["units"][i]
            if unitdata:
                unittype =  GridElementFactory.find_unit_class(unitdata["name"])
                if unittype:
                    unit = self.add_unit(
                        self.i_to_c(i), 
                        UNIT_IDS.index(unitdata["name"]), 
                        unitdata["ownerid"]
                    )
                    unit.insert_data(unitdata)
        for i in range(len(data["worldeffects"])):
            effectstackdata = data["worldeffects"][i]
            for effectdata in effectstackdata:
                effecttype = GridElementFactory.find_effect_class(effectdata["name"])
                if effecttype:
                    self.add_worldeffect(
                        self.i_to_c(i), 
                        EFFECT_IDS.index(effectdata["name"]), 
                        True)
        
        
    def update_observer(self, observer:Optional[IGridObserver]):
        """
        Set a new observer, which will receive events for e.g. a spawned unit.

        Useful in event-based scenarios, like loading a graphical display for the new unit.
        """
        self.observer = observer
    
    def everybody_done(self) -> bool:
        """Check whether every member of the grid has finished it's actions, like moving."""
        for group in (self.units, self.tiles):    
            for member in group:
                if member and not member.done:
                    return False
        for effectstack in self.worldeffects:    
            for effect in effectstack:
                if effect and not effect.done:
                    return False
        return True

    def update_unit_movement(self):
        """Move units by one step and handle collisions between them or other obstacles. Server Only"""
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
                    unit.get_movement_ability().on_trigger()
                    movingunits.append(unit)
        if len(movingunits) > 0:
            nextpositions:dict[tuple[int,int],list[UnitBase]] = {} #position:[units that want to go here]
            # remove units whose path is already exhausted
            # and add their positions into obstacles
            for unit in movingunits[:]:
                path = unit.get_movement_ability().selected_targets
                if len(path) == 0:
                    movingunits.remove(unit)
                    unit.done = True
                    unit.get_movement_ability().selected_targets.clear()
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
        self.change_phase(nextphase)

    def load_map(self, map:Map, from_authority:bool):
        """Load a map, spawning all the required units, tiles, etc.."""
        if self.observer:
            self.observer.on_load_map(map)
        self.width = map.width
        self.height = map.height
        c = self.width*self.height
        self.tiles = [None]*c
        self.units = [None]*c
        self.worldeffects = [[] for i in range(c)]
        self.uniteffects = [[] for i in range(c)]
        for pos, tileid, tileeffectids, uniteffectids, unitid in map.iterate_tiles():
            if tileid:
                self.add_tile(pos, tileid)
            if tileeffectids:
                for tileeffectid in tileeffectids:
                    self.add_worldeffect(pos, tileeffectid, from_authority=from_authority, use_net=False)
            if uniteffectids:
                for uniteffectid in uniteffectids:
                    self.add_uniteffect(pos, uniteffectid, from_authority=from_authority, use_net=False)
            if unitid:
                self.add_unit(pos, unitid, -1)

    def add_tile(self, pos:"tuple[int,int]", tileid:int) -> bool:
        """Add a tile to the grid at given position."""
        tiletype = GridElementFactory.find_tile_class(TILE_IDS[tileid])
        newtile = tiletype(self, pos)
        index = self.c_to_i(pos)
        if index >= 0 and index < len(self.tiles):
            self.tiles[self.c_to_i(pos)] = newtile
            if self.observer:
                self.observer.on_add_tile(newtile)
            return True
        print("Grid: Tried to add tile at index", index, "which is out if range.")
        return False

    def add_worldeffect(self, pos:"tuple[int,int]", tileeffectid:int, from_authority:bool, use_net=True):
        """Add an tile effect to the grid at given position."""
        if from_authority:
            effecttype:EffectBase = GridElementFactory.find_effect_class(EFFECT_IDS[tileeffectid])     
            neweffect:EffectBase = effecttype(self, pos)
            self.worldeffects[self.c_to_i(pos)].append(neweffect)
            if self.observer:
                self.observer.on_add_worldeffect(neweffect)
            if use_net and NetEvents.connector.authority:
                NetEvents.snd_neteffectspawn(tileeffectid, pos)
            neweffect.on_spawn()
        else:
            pass #NetEvents.snd_neteffectspawn(effectid, pos)

    def request_add_unit(self, x, y, unitid:int, playerid:int):
        NetEvents.snd_netunitspawn(unitid, (x,y), playerid)

    def add_unit(self, pos:"tuple[int,int]", unitid:int, ownerid:int) -> Optional[UnitBase]:
        """Add a unit to the grid at given position, owned by ownerid."""
        unitclass = GridElementFactory.find_unit_class(UNIT_IDS[unitid])
        newunit = unitclass(self, pos, ownerid)
        index = self.c_to_i(pos)
        if index >= 0 and index < len(self.units):
            self.units[index] = newunit
            if self.observer:
                self.observer.on_add_unit(newunit)
            return newunit
        print("Grid: Tried to add unit at index", index, "which is out if range.")
        return None

    def remove_unit(self, pos:"tuple[int,int]"):
        """Remove a unit at given position."""
        if self.is_space_empty(False, pos):
            print(f"Grid: Tried to remove unit at {pos}, which is empty.")
            return False
        elif NetEvents.connector and NetEvents.connector.authority:
            NetEvents.snd_netunitremove(pos)
        self.units[self.c_to_i(pos)] = None
        if self.observer:
            self.observer.on_remove_unit(pos)
        return True
    
    def remove_tileeffect(self, effect:"EffectBase", pos:"tuple[int,int]"):
        """Remove an effect at given position."""
        self.worldeffects[self.c_to_i(pos)].remove(effect)
        if self.observer:
            self.observer.on_remove_tileeffect(effect, pos)

    def move_unit(self, from_pos:"tuple[int,int]", to_pos:"tuple[int,int]") -> bool:
        """Move a unit from (x,y) to (tagretx,targety)."""
        if self.is_space_empty(False, from_pos):
            print(f"Grid: Tried to move unit at {from_pos} which does not exist.")
            return False
        if not self.is_space_empty(True, to_pos):
            unit = self.get_unit(from_pos)
            self.units[self.c_to_i(from_pos)] = None
            self.units[self.c_to_i(to_pos)] = unit
            unit.pos = to_pos
            NetEvents.snd_netunitmove(from_pos, to_pos)
            self.tiles[self.c_to_i(to_pos)].on_enter(unit)
            if self.observer:
                self.observer.on_move_unit(from_pos, to_pos)
            return True
        else:
            print(f"Grid: Unit would have fallen from the grid at {to_pos}.")
            return False

    def get_tile(self, pos:"tuple[int,int]"):
        """Return the tile at (x,y)."""
        return self.tiles[self.c_to_i(pos)]
   
    def get_tileeffects(self, pos:"tuple[int,int]"):
        """Return the tile effects at (x,y)."""
        return self.worldeffects[self.c_to_i(pos)]
   
    def get_unit(self, pos:"tuple[int,int]") -> "Optional[UnitBase]":
        """Return the unit at (x,y)."""
        i = self.c_to_i(pos)
        if i >= 0 and i < len(self.units) :
            return self.units[i]
        else:
            return None

    def c_to_i(self, coords:"tuple[int,int]") -> int:
        """Convert xy-coordinates to the corresponding index."""
        return self.width*coords[1] + coords[0]
    
    def i_to_c(self, i:int) -> "tuple[int,int]":
        """Convert index to the corresponding xy-coordinates."""
        return (i%self.width, int(i/self.width))

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
        for wes in self.worldeffects:
            for e in wes:
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
            elif self.phase in [2,3]:
                if self.everybody_done():
                    self.advance_phase()
                    NetEvents.snd_netphasechange(self.phase)
            elif self.phase == 4:
                print("test")
                if self.everybody_done():
                    self.advance_phase()
                    NetEvents.snd_netphasechange(self.phase)
                    NetEvents.snd_netsync()
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
                    text += str(tile.name)+" "
                else:
                    text += " "
            text += "\n"
        print(text)
