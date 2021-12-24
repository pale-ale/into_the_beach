from itblib.globals.Enums import EFFECT_IDS, PHASES, TILE_IDS, UNIT_IDS
from itblib.globals.GridElementFactory import GridElementFactory
from itblib.gridelements.Effects import EffectBase
from itblib.gridelements.GridElement import GridElement
from itblib.gridelements.Tiles import TileBase
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.Maps import Map
from itblib.net.Connector import Connector
from itblib.net.NetEvents import NetEvents
from itblib.Serializable import Serializable

from .ui.IGridObserver import IGridObserver


class Grid(Serializable):
    """Manager for Data-Only-Objects like units, tiles, effects, etc."""

    def __init__(self, connector:Connector, observer:"IGridObserver|None"=None, width:int=10, height:int=10):
        super().__init__(["size", "phasetime", "tiles", "units", "worldeffects"])
        self.remake_grid(width, height)
        self.worldeffects:"list[list[EffectBase]]" = [[] for i in range(width*height)]
        self.phasetime = 0
        self.gametime = 0
        self.connector = connector
        self.planningphasetime = 10
        self.pregametime = 10
        self.observer = observer
        self.phase = 0
    
    def remake_grid(self, width, height) -> None:
        """Empty the grid lists and create new ones with the given dimensions."""
        self.size:"tuple[int,int]" = (width, height)
        c = width * height
        self.tiles:"list[TileBase|None]" = [None]*c
        self.units:"list[UnitBase|None]" = [None]*c
        #self.worldeffects:"list[list[EffectBase]]" = [[] for i in range(c)]
    
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
                "worldeffects":customworldeffects,
                "size":self.size
            }
        )
    
    
    def insert_data(self, data) -> None:
        """Insert the received data into the grid, creating and configuring new units, tiles, etc. accordingly.
        Clears the grid beforehand."""
        # TODO: constructing everything every turn might be a bit much, maybe moving
        # units around is a better way to go performance-wise...
        self.phasetime = data["phasetime"]
        new_x, new_y = data["size"]
        new_count:int = new_x * new_y
        new_tiles:"list[TileBase|None]" = [None]*new_count
        new_units:"list[UnitBase|None]" = [None]*new_count
        old_tiles = self.tiles
        old_units = self.units
        self.tiles = new_tiles
        self.units = new_units
        self.remake_grid(new_x, new_y)
        self.size = (new_x, new_y)

        for i in range(len(data["tiles"])):
            tiledata = data["tiles"][i]
            if tiledata:
                tiletype = GridElementFactory.find_tile_class(tiledata["name"])
                pos = self.i_to_c(i)
                existing_tile = old_tiles[i]
                if isinstance(existing_tile, tiletype):
                    self.tiles[i] = old_tiles[i]
                elif tiletype:
                    self.add_tile(
                        pos, 
                        TILE_IDS.index(tiledata["name"])
                    )

        for i in range(len(data["units"])):
            unitdata = data["units"][i]
            if unitdata:
                name = unitdata["name"]
                if name != "None":
                    unittype =  GridElementFactory.find_unit_class(unitdata["name"])
                    pos = self.i_to_c(i)
                    existing_unit = old_units[i]
                    if isinstance(existing_unit, unittype):
                        self.units[i] = old_units[i]
                        self.units[i].insert_data(unitdata)
                    elif unittype:
                        self.add_unit(
                            self.i_to_c(i), 
                            UNIT_IDS.index(unitdata["name"]), 
                            unitdata["ownerid"]
                        ).insert_data(unitdata)
        self._insert_effect_data(data)

    def _insert_effect_data(self, effect_data):
        new_effects:"list[list[EffectBase]]" = [[] for c in range(self.size[0]*self.size[1])]
        old_effects = self.worldeffects
        self.worldeffects = new_effects

        for i in range(len(effect_data["worldeffects"])):
            effect_stack_data = effect_data["worldeffects"][i]
            for effect_data_index in range(len(effect_stack_data)):
                single_effect_data = effect_stack_data[effect_data_index]
                effect_type = GridElementFactory.find_effect_class(single_effect_data["name"])
                pos = self.i_to_c(i)
                existing_stack = old_effects[i]
                if effect_data_index < len(existing_stack):
                    existing_effect = existing_stack[effect_data_index]
                    if type(existing_effect) == effect_type:
                        self.worldeffects[i].append(old_effects[i][effect_data_index])
                        continue
                self.add_worldeffect(
                    pos, 
                    EFFECT_IDS.index(single_effect_data["name"])
                )
        
    def update_observer(self, observer:"IGridObserver|None") -> None:
        """
        Set a new observer, which will receive events for e.g. a spawned unit.

        Useful in event-based scenarios, like loading a graphical display for the new unit.
        """
        self.observer = observer
    
    def everybody_done(self) -> bool:
        """Check whether every member of the grid has finished it's actions, like moving."""
        notdone = []
        for group in (self.units, self.tiles):    
            for member in group:
                if member and not member.done:
                    notdone.append(member)
        for effectstack in self.worldeffects:    
            for effect in effectstack:
                if effect and not effect.done:
                    notdone.append(member)
        return len(notdone) == 0

    def update_unit_movement(self) -> None:
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

    def change_phase(self, phase) -> None:
        """Set the phase to a certain number."""
        self.phase = phase
        self.phasetime = 0
        if self.observer:
            self.observer.on_change_phase(phase)
        for element in self.tiles:
            if element:
                element.on_update_phase(self.phase)
        for element in self.units:
            if element:
                element.on_update_phase(self.phase)
        for elements in self.worldeffects:
            for element in elements:
                element.on_update_phase(self.phase)

    def advance_phase(self) -> None:
        """Advance phase cycle by one, starting from the planning phase once the end is reached."""
        maxphase = len(PHASES)-1
        nextphase = (self.phase)%maxphase+1
        self.change_phase(nextphase)

    def load_map(self, map:Map, from_authority:bool) -> None:
        """Load a map, spawning all the required units, tiles, etc.."""
        if self.observer:
            self.observer.on_load_map(map)
        self.remake_grid(map.width, map.height)
        for pos, tileid, tileeffectids, unitid in map.iterate_tiles():
            if tileid:
                self.add_tile(pos, tileid)
            if tileeffectids:
                for tileeffectid in tileeffectids:
                    self.add_worldeffect(pos, tileeffectid)
            if unitid:
                self.add_unit(pos, unitid, -1)

    def add_gridelement(self, pos:"tuple[int,int]", gridelement:GridElement) -> "TileBase|UnitBase|EffectBase|None":
        """Helper to add an object at pos to the grid."""
        if not self.is_coord_in_bounds(pos):
            print("Grid: Tried to add element at", pos, "which is not on the grid.")
            return None
        index = self.c_to_i(pos)
        if isinstance(gridelement, TileBase):
            self.tiles[index] = gridelement
            if self.observer:
                self.observer.on_add_tile(gridelement)
        elif isinstance(gridelement, EffectBase):
            self.worldeffects[index].append(gridelement)
            if self.observer:
                self.observer.on_add_worldeffect(gridelement)
        elif isinstance(gridelement, UnitBase):
            self.units[index] = gridelement
            if self.observer:
                self.observer.on_add_unit(gridelement)
        else:
            exit(1)
        return gridelement

    def add_tile(self, pos:"tuple[int,int]", tileid:int) -> "TileBase|None":
        """Add a tile to the grid at given position."""
        tiletype:TileBase = GridElementFactory.find_tile_class(TILE_IDS[tileid])
        newtile:TileBase = tiletype(self, pos)
        return self.add_gridelement(pos, newtile)

    def add_worldeffect(self, pos:"tuple[int,int]", worldeffectid:int) -> "TileBase|None":
        """Add a world effect to the grid at given position."""
        effecttype:EffectBase = GridElementFactory.find_effect_class(EFFECT_IDS[worldeffectid])     
        neweffect:EffectBase = effecttype(self, pos)
        neweffect.on_spawn()
        return self.add_gridelement(pos, neweffect)

    def add_unit(self, pos:"tuple[int,int]", unitid:int, ownerid:int) -> "UnitBase|None":
        """Add a unit to the grid at given position, owned by ownerid."""
        unittype:UnitBase = GridElementFactory.find_unit_class(UNIT_IDS[unitid])
        newunit:UnitBase = unittype(self, pos, ownerid)
        return self.add_gridelement(pos, newunit) 

    def request_add_unit(self, pos:"tuple[int,int]", unitid:int, playerid:int) -> None:
        """Request a unit with unitid to be spawned at (x,y), owned by a playerid."""
        NetEvents.snd_netunitspawn(unitid, pos, playerid)
    
    def remove_gridelement(self, pos:"tuple[int,int]", effect:"EffectBase|None"=None, rmflags=0b100) -> bool:
        """Remove a gridelement at given position. 
        Use the flags to specify Tiles, Units, and Effects respectively.
        When removing effects, effect shouldn't be None."""
        tiles = rmflags & 0b100
        units = rmflags & 0b010
        effects = rmflags & 0b001
        if not self.is_coord_in_bounds(pos):
            print("Grid: Tried to remove element at", pos, "which is not on the grid.")
            return False
        if tiles and self.is_space_empty(True, pos):
            print("Grid: Tried to remove tile at", pos, "which is empty.")
            return False
        if units and self.is_space_empty(False, pos):
            print("Grid: Tried to remove unit at", pos, "which is empty.")
            return False
        index = self.c_to_i(pos)
        if effects:
            if effect not in self.worldeffects[index]:
                print("Grid: Tried to remove effect", effect, "at", pos, "which is does not exist.")
                return False

        if tiles:
            self.tiles[index] = None
            if self.observer:
                self.observer.on_remove_tile(pos)
        if units:
            self.units[index] = None
            if self.observer:
                self.observer.on_remove_unit(pos)
        if effects:
            self.worldeffects[index].remove(effect)
            if self.observer:
                self.observer.on_remove_worldeffect(effect, pos)
        return True

    def remove_tile(self, pos:"tuple[int,int]") -> bool:
        """Remove a unit at given position."""
        return self.remove_gridelement(pos, rmflags=0b100)
    
    def remove_unit(self, pos:"tuple[int,int]") -> bool:
        """Remove a unit at given position."""
        return self.remove_gridelement(pos, rmflags=0b010)
    
    def remove_worldeffect(self, effect:"EffectBase", pos:"tuple[int,int]") -> bool:
        """Remove an effect at given position."""
        return self.remove_gridelement(pos, effect=effect, rmflags=0b001)

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
            self.tiles[self.c_to_i(to_pos)].on_enter(unit)
            if self.observer:
                self.observer.on_move_unit(from_pos, to_pos)
            return True
        else:
            print(f"Grid: Unit would have fallen from the grid at {to_pos}.")
            return False

    def get_tile(self, pos:"tuple[int,int]") -> "TileBase|None":
        """Return the tile at (x,y)."""
        return self.tiles[self.c_to_i(pos)]
   
    def get_worldeffects(self, pos:"tuple[int,int]") -> "list[EffectBase]":
        """Return the world effects at (x,y)."""
        return self.worldeffects[self.c_to_i(pos)]
   
    def get_unit(self, pos:"tuple[int,int]") -> "UnitBase|None":
        """Return the unit at (x,y)."""
        i = self.c_to_i(pos)
        if i >= 0 and i < len(self.units) :
            return self.units[i]
        else:
            return None

    def c_to_i(self, coords:"tuple[int,int]") -> int:
        """Convert xy-coordinates to the corresponding index."""
        return self.size[0]*coords[1] + coords[0]
    
    def i_to_c(self, i:int) -> "tuple[int,int]":
        """Convert index to the corresponding xy-coordinates."""
        return (i%self.size[0], int(i/self.size[0]))

    def is_coord_in_bounds(self, pos:"tuple[int,int]") -> bool:
        """Check whether a coordinate is inside the grid space."""
        return pos[0]>=0 and pos[0]<self.size[0] and pos[1]>=0 and pos[1]<self.size[1]

    def is_space_empty(self, tiles:bool, pos:"tuple[int,int]") -> bool:
        """Check whether a tile or a unit is at the given position."""
        return self.is_coord_in_bounds(pos) and \
            not (self.tiles if tiles else self.units)[self.c_to_i(pos)]

    def get_ordinal_neighbors(self, pos:"tuple[int,int]") -> "list[tuple[int,int]]":
        """Returns the coordinates of neighboring tiles when inside bounds."""
        x,y = pos
        up = (x-1,y)
        right = (x,y+1)
        down = (x+1,y)
        left = (x,y-1)
        return [n for n in (up, right, down, left) if self.is_coord_in_bounds(n)]

    def tick(self, dt:float) -> None:
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
                    NetEvents.snd_netsync()
                    self.advance_phase()
                    NetEvents.snd_netphasechange(self.phase)
                    self.phasetime = 0.0
            elif self.phase in [2,3]:
                if self.everybody_done():
                    self.advance_phase()
                    NetEvents.snd_netphasechange(self.phase)
            elif self.phase == 4:
                if self.everybody_done():
                    self.advance_phase()
                    NetEvents.snd_netphasechange(self.phase)
                    NetEvents.snd_netsync()
                else:
                    if self.phasetime >= 0.5:
                        self.phasetime = 0.0
                        self.update_unit_movement()
        else:
            if self.phase == 4:
                if not self.everybody_done():
                    if self.phasetime >= 0.5:
                        self.phasetime = 0.0
                        self.update_unit_movement()

    def show(self) -> None:
        """Print the grid onto the console."""
        text = ""
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                tile = self.tiles[self.size[0]*y+x]
                if tile:
                    text += str(tile.name)+" "
                else:
                    text += " "
            text += "\n"
        print(text)
