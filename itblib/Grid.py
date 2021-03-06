from typing import TYPE_CHECKING
from itblib.Vec import IVector2

from itblib.globals.Enums import EFFECT_IDS, PHASES, TILE_IDS, UNIT_IDS
from itblib.globals.factories import GridElementFactory
from itblib.gridelements.GridElement import GridElement
from itblib.gridelements.Tiles import TileBase
from itblib.gridelements.units.UnitBase import UnitBase
from itblib.gridelements.world_effects import WorldEffectBase
from itblib.Log import log
from itblib.Maps import Map
from itblib.net.Connector import Connector
from itblib.net.NetEvents import NetEvents
from itblib.Serializable import Serializable

if TYPE_CHECKING:
    from itblib.ui.IGridObserver import IGridObserver


class Grid(Serializable):
    """Manager for Data-Only-Objects like units, tiles, effects, etc."""

    def __init__(self, connector:Connector, observer:"IGridObserver|None"=None, width:int=10, height:int=10):
        super().__init__(["size", "phasetime", "tiles", "units", "worldeffects"])
        self.phasetime = 0
        self.gametime = 0
        self.connector = connector
        self.planningphasetime = 10
        self.pregametime = 10
        self.observer = observer
        self.phase = 0
        self.remake_grid(width, height)
        self.worldeffects:"list[list[WorldEffectBase]]" = [[] for i in range(width*height)]
    
    def remake_grid(self, width, height) -> None:
        """Empty the grid lists and create new ones with the given dimensions."""
        self.size: IVector2 = IVector2(width, height)
        c = width * height
        self.tiles:"list[TileBase|None]" = [None]*c
        self.units:"list[UnitBase|None]" = [None]*c
        if self.observer:
            self.observer.on_remake_grid()
        #self.worldeffects:"list[list[WorldEffectBase]]" = [[] for i in range(c)]
    
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
                "size":self.size.c
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
        self.size = IVector2(new_x, new_y)

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
        new_effects:"list[list[WorldEffectBase]]" = [[] for c in range(self.size.x*self.size.y)]
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
                ).insert_data(single_effect_data, [])
        
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
                    obstacles.append(unit.position)
                    unit.done = True
                else:
                    unit.get_movement_ability().on_trigger()
                    movingunits.append(unit)
        if len(movingunits) > 0:
            nextpositions:dict[IVector2,list[UnitBase]] = {} #position:[units that want to go here]
            # remove units whose path is already exhausted
            # and add their positions into obstacles
            for unit in movingunits[:]:
                path = unit.get_movement_ability().selected_targets
                if len(path) == 0:
                    movingunits.remove(unit)
                    unit.done = True
                    unit.get_movement_ability().selected_targets.clear()
                    obstacles.append(unit.position)
            # add each unit and their next move to the dict
            # and remove first path element
            for unit in movingunits[:]:
                nextpos = unit.get_movement_ability().selected_targets.pop(0)
                assert isinstance(nextpos, IVector2)
                if nextpos in obstacles:
                    movingunits.remove(unit)
                    unit.done = True
                    obstacles.append(unit.position)
                if nextpos in nextpositions:
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
                            obstacles.append(unit.position)
                            unit.done = True
                elif len(units) == 1:
                    self.move_unit(units[0].position, position)

    def change_phase(self, phase:int) -> None:
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
        maxphase = PHASES._MAX-1
        nextphase = (self.phase)%maxphase+1
        self.change_phase(nextphase)

    def load_map(self, new_map:Map) -> None:
        """Load a map, spawning all the required units, tiles, etc.."""
        self.remake_grid(new_map.width, new_map.height)
        for coords, tileid, tileeffectids, unitid in new_map.iterate_tiles():
            position = IVector2(*coords)
            if tileid:
                self.add_tile(position, tileid)
            if tileeffectids:
                for tileeffectid in tileeffectids:
                    self.add_worldeffect(position, tileeffectid)
            if unitid:
                self.add_unit(position, unitid, -1)

    def add_gridelement(self, pos: IVector2, gridelement: GridElement) -> "TileBase|UnitBase|WorldEffectBase|None":
        """Helper to add an object at pos to the grid."""
        if not self.is_coord_in_bounds(pos):
            log("Grid: Tried to add element at", pos, "which is not on the grid.", 2)
            return None
        index = self.c_to_i(pos)
        if isinstance(gridelement, TileBase):
            self.tiles[index] = gridelement
            if self.observer:
                self.observer.on_add_tile(gridelement)
        elif isinstance(gridelement, WorldEffectBase):
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

    def add_tile(self, pos: IVector2, tileid: int) -> "TileBase|None":
        """Add a tile to the grid at given position."""
        tiletype:TileBase = GridElementFactory.find_tile_class(TILE_IDS[tileid])
        newtile:TileBase = tiletype(self, pos)
        return self.add_gridelement(pos, newtile)

    def add_worldeffect(self, pos: IVector2, worldeffectid:int) -> "WorldEffectBase|None":
        """Add a world effect to the grid at given position."""
        effecttype:WorldEffectBase = GridElementFactory.find_effect_class(EFFECT_IDS[worldeffectid])     
        neweffect:WorldEffectBase = effecttype(self, pos)
        neweffect.on_spawn()
        return self.add_gridelement(pos, neweffect)

    def add_unit(self, pos: IVector2, unitid:int, ownerid:int) -> "UnitBase|None":
        """Add a unit to the grid at given position, owned by ownerid."""
        unittype:UnitBase = GridElementFactory.find_unit_class(UNIT_IDS[unitid])
        newunit:UnitBase = unittype(self, pos, ownerid)
        return self.add_gridelement(pos, newunit)

    def request_add_unit(self, pos: IVector2, unitid:int, playerid:int) -> None:
        """Request a unit with unitid to be spawned at (x,y), owned by a playerid."""
        NetEvents.snd_netunitspawn(unitid, pos.c, playerid)
    
    def remove_gridelement(self, pos: IVector2, effect:"WorldEffectBase|None"=None, rmflags=0b100) -> bool:
        """Remove a gridelement at given position. 
        Use the flags to specify Tiles, Units, and Effects respectively.
        When removing effects, effect shouldn't be None."""
        tiles = rmflags & 0b100
        units = rmflags & 0b010
        effects = rmflags & 0b001
        if not self.is_coord_in_bounds(pos):
            log(f"Grid: Tried to remove element at {pos} which is not on the grid.", 2)
            return False
        if tiles and self.is_space_empty(True, pos):
            log(f"Grid: Tried to remove tile at {pos} which is empty.", 2)
            return False
        if units and self.is_space_empty(False, pos):
            log(f"Grid: Tried to remove unit at {pos} which is empty.", 2)
            return False
        index = self.c_to_i(pos)
        if effects:
            if effect not in self.worldeffects[index]:
                log("Grid: Tried to remove effect", effect, "at", pos, "which is does not exist.", 2)
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

    def remove_tile(self, pos: IVector2) -> bool:
        """Remove a unit at given position."""
        return self.remove_gridelement(pos, rmflags=0b100)
    
    def remove_unit(self, pos: IVector2) -> bool:
        """Remove a unit at given position."""
        return self.remove_gridelement(pos, rmflags=0b010)
    
    def remove_worldeffect(self, effect:"WorldEffectBase", pos: IVector2) -> bool:
        """Remove an effect at given position."""
        return self.remove_gridelement(pos, effect=effect, rmflags=0b001)

    def move_unit(self, from_pos: IVector2, to_pos: IVector2) -> bool:
        """Move a unit at from_pos to to_pos."""
        if self.is_space_empty(False, from_pos):
            log(f"Grid: Tried to move unit at {from_pos} which does not exist.", 2)
            return False
        if not self.is_space_empty(True, to_pos):
            unit = self.get_unit(from_pos)
            self.units[self.c_to_i(from_pos)] = None
            self.units[self.c_to_i(to_pos)] = unit
            unit.position = to_pos
            self.tiles[self.c_to_i(to_pos)].on_enter(unit)
            if self.observer:
                self.observer.on_move_unit(from_pos, to_pos)
            return True
        else:
            log(f"Grid: Unit would have fallen from the grid at {to_pos}.", 0)
            return False

    def get_tile(self, pos: IVector2) -> "TileBase|None":
        """Return the tile at (x,y)."""
        return self.tiles[self.c_to_i(pos)]
   
    def get_worldeffects(self, pos: IVector2) -> "list[WorldEffectBase]":
        """Return the world effects at (x,y)."""
        return self.worldeffects[self.c_to_i(pos)]
   
    def get_unit(self, pos: IVector2) -> "UnitBase|None":
        """Return the unit at (x,y)."""
        i = self.c_to_i(pos)
        if i >= 0 and i < len(self.units) :
            return self.units[i]
        else:
            return None

    def c_to_i(self, coords: IVector2) -> int:
        """Convert xy-coordinates to the corresponding index."""
        return self.size.x*coords.y + coords.x
    
    def i_to_c(self, i:int) ->  IVector2:
        """Convert index to the corresponding xy-coordinates."""
        return IVector2(i%self.size.x, int(i/self.size.y))

    def is_coord_in_bounds(self, pos: IVector2) -> bool:
        """Check whether a coordinate is inside the grid space."""
        return pos.x >=0 and pos.x < self.size.x and pos.y >= 0 and pos.y < self.size.y

    def is_space_empty(self, tiles:bool, pos: IVector2) -> bool:
        """Check whether a tile or a unit is at the given position."""
        return self.is_coord_in_bounds(pos) and \
            not (self.tiles if tiles else self.units)[self.c_to_i(pos)]

    def get_neighbors(self, pos: IVector2, ordinal=True, cardinal=False) -> "list[IVector2]":
        """Returns the coordinates of neighboring tiles when inside bounds."""
        x,y = pos
        tiles_to_check:list[tuple[int,int]] = list()
        ordinals = [(x-1,y), (x,y+1), (x+1,y), (x,y-1)]
        cardinals = [(x-1,y-1), (x-1,y+1), (x+1,y+1), (x+1,y-1)]
        lists = []
        if cardinal:
            lists.append(cardinals)
        if ordinal:
            lists.append(ordinals)
        tiles_to_check = [elem for tup in zip(*lists) for elem in tup]
        result = []
        for n_coords in tiles_to_check:
            n_vector = IVector2(*n_coords)
            if self.is_coord_in_bounds(n_vector):
                result.append(n_vector)
        return result

    def get_ordinals(self, origin: IVector2, dimensions: IVector2):
        """Return the coordinates aling the ordinal lines of origin, up to dimensions in length."""
        max_x, max_y = origin
        ordinals:"set[tuple[int,int]]" = set()
        for i in range (dimensions[0]):
            ordinals.add((i,max_y))
        for i in range (dimensions[1]):
            ordinals.add((max_x,i))
        ordinals.remove((max_x,max_y))
        return ordinals

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
        if self.connector and self.connector.authority:
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
