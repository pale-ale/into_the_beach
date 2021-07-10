from itblib.gridelements.GridElement import GridElement
from typing import Optional
from itblib.net.Connector import Connector
from .gridelements.Tiles import TileBase
from .gridelements.Effects import EffectBase
from .gridelements.Units import UnitBase
from .Maps import Map

from .Globals import ClassMapping
from .Enums import PHASES
from .ui.IGridObserver import IGridObserver
from .net import NetEvents

import random

class Grid:
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
        self.observer = observer
    
    def everybody_done(self) -> bool:
        for group in (self.units, self.tiles, self.effects):    
            for member in group:
                if member and not member.done:
                    return False
        return True

    def update_unit_movement(self):
        movingunits:"list[UnitBase]" = []
        obstacles:"list[GridElement]" = []
        #filter units that cannot move
        for unit in self.units:
            if unit:
                if not "MovementAbility" in unit.abilities.keys() or \
                len(unit.abilities["MovementAbility"].selected_targets) == 0:
                    obstacles.append(unit.get_position())
                    unit.done = True
                else:
                    movingunits.append(unit)
        if len(movingunits) > 0:
            nextpositions = {} #position:[units that want to go here]
            # remove units whose path is already exhausted
            # and add their positions into obstacles
            for unit in movingunits[:]:
                path = unit.abilities["MovementAbility"].selected_targets
                if len(path) == 0:
                    movingunits.remove(unit)
                    unit.done = True
                    obstacles.append(unit.get_position())
            # add each unit and their next move to the dict
            # and remove first path element
            for unit in movingunits[:]:
                nextpos = unit.abilities["MovementAbility"].selected_targets.pop(0)[0]
                print(nextpos)
                if nextpos in obstacles:
                    movingunits.remove(unit)
                    unit.done = True
                    obstacles.append(unit.get_position())
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
                            obstacles.append(unit.get_position())
                            unit.done = True
                elif len(units) == 1:
                    self.move_unit(*units[0].get_position(), *position)


    def advance_phase(self):
        maxphase = len(PHASES)-1
        self.phase = (self.phase)%maxphase+1
        print("next phase...")
        for unit in self.units:
            if unit:
                unit.trigger_hook("OnUpdatePhase", self.phase)
    
    def change_phase(self, phase):
        self.phase = phase
        self.phasetime = 0
        for unit in self.units:
            if unit:
                unit.trigger_hook("OnUpdatePhase", self.phase)

    def load_map(self, map:Map):
        if self.observer:
            self.observer.on_load_map(map)
        self.width = map.width
        self.height = map.height
        self.tiles = [None]*self.width*self.height
        self.units = [None]*self.width*self.height
        self.effects = [None]*self.width*self.height
        for x, y, tileid, effectid, unitid in map.iterate_tiles():
            if tileid:
                self.add_tile(x, y, tiletype=ClassMapping.tileclassmapping[tileid])
            if effectid:
                self.add_effect(x, y, effecttype=ClassMapping.effectclassmapping[effectid])
            if unitid:
                self.add_unit(x, y, unittype=ClassMapping.unitclassmapping[unitid])

    def add_tile(self, x:int, y:int, tiletype:TileBase=TileBase):
        assert issubclass(tiletype, TileBase)
        newtile = tiletype()
        newtile.set_position((x,y))
        self.tiles[self.width*y+x] = newtile
        if self.observer:
            self.observer.on_add_tile(newtile)

    def add_effect(self, x:int, y:int, effecttype:EffectBase=EffectBase):
        assert issubclass(effecttype, EffectBase)
        neweffect = effecttype()
        neweffect.set_position((x,y))
        self.effects[self.width*y+x] = neweffect
        if self.observer:
            self.observer.on_add_effect(neweffect)

    def request_add_unit(self, x, y, unitid:int, playerid:int):
        NetEvents.snd_netunitspawn(unitid, (x,y), playerid)

    def add_unit(self, x, y, unitid:int, ownerid:int):
        unitclass = ClassMapping.unitclassmapping[unitid]
        newunit = unitclass(self, ownerid)
        newunit.set_position((x, y))
        self.units[self.width*y+x] = newunit
        if self.observer:
            self.observer.on_add_unit(newunit)

    def remove_unit(self, x:int, y:int):
        if self.is_space_empty(False, x, y):
            print(f"error try to remove unit at {x} {y} which does not exist.")
            exit(1)
        self.units[self.width*y+x] = None
        self.observer.on_remove_unit(x, y)
    
    def move_unit(self, x:int, y:int, targetx:int, targety:int):
        if self.is_space_empty(False, x, y):
            print(f"error try to move unit at {x} {y} which does not exist.")
            exit(1)    
        if self.is_space_empty(False, targetx, targety) and not \
                self.is_space_empty(True, targetx, targety):
            unit = self.units[self.width*y+x]
            self.units[self.width*y+x] = None
            self.units[self.width*targety+targetx] = unit
            unit.set_position((targetx, targety))
            NetEvents.snd_netunitmove((x,y), (targetx, targety))
            self.tiles[self.width*targety+targetx].on_enter(unit)
            if self.observer:
                self.observer.on_move_unit(x, y, targetx, targety)

    def get_tile(self, x:int, y:int):
        return self.tiles[self.width*y+x]
   
    def get_effect(self, x:int, y:int):
        return self.effects[self.width*y+x]
    
    def get_unit(self, x:int, y:int):
        return self.units[self.width*y+x]

    def c_to_i(self, x, y):
        return self.width*y + x

    def is_coord_in_bounds(self, x, y):
        assert isinstance(x,int) and isinstance(y,int)
        return x>=0 and x<self.width and y>=0 and y<self.height

    def is_space_empty(self, tiles:bool, x:int, y:int)->bool:
        return self.is_coord_in_bounds(x,y) and not (self.tiles if tiles else self.units)[self.width*y+x]

    def get_ordinal_neighbors(self, x, y):
        assert isinstance(x, int) and isinstance(y, int)
        up = (x-1,y)
        right = (x,y+1)
        down = (x+1,y)
        left = (x,y-1)
        return [n for n in (up, right, down, left) if self.is_coord_in_bounds(*n)]

    def tick(self, dt:float):
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
