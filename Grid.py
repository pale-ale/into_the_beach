from Tiles import TileBase
from Effects import EffectBase
from Units import UnitBase
from Maps import Map

from Globals import Classes
from IGridObserver import IGridObserver

class Grid:
    def __init__(self, observer=None, width:int=10, height:int=10):
        self.height = width
        self.width = height
        self.tiles = [None]*width*height
        self.units = [None]*width*height
        self.effects = [None]*width*height
        self.observer = observer

    def update_observer(self, observer):
        self.observer = observer

    def load_map(self, map:Map):
        for x, y, tileid, effectid, unitid in map.iterate_tiles():
            if tileid is not None:
                self.add_tile(x, y, tiletype=Classes.tileclassmapping[tileid])
            if effectid is not None:
                self.add_effect(x, y, effecttype=Classes.effectclassmapping[effectid])
            if unitid is not None:
                self.add_unit(x, y, unittype=Classes.unitclassmapping[unitid])

    def add_tile(self, x:int, y:int, tiletype:TileBase=TileBase):
        assert issubclass(tiletype, TileBase)
        newtile = tiletype()
        newtile.pos = [x,y]
        self.tiles[self.width*y+x] = newtile
        self.observer.on_add_tile(newtile)

    def add_effect(self, x:int, y:int, effecttype:EffectBase=EffectBase):
        assert issubclass(effecttype, EffectBase)
        neweffect = effecttype()
        neweffect.pos = [x,y]
        self.effects[self.width*y+x] = neweffect
        self.observer.on_add_effect(neweffect)

    def add_unit(self, x, y, unittype:UnitBase=UnitBase):
        newunit = unittype(grid=self, name=" ")
        newunit.pos = [x, y]
        self.units[self.width*y+x] = newunit
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
            unit = self.units.pop(self.width*y+x)
            self.units[self.width*targety+targetx] = unit
            unit.pos = [targetx, targety]
            self.tiles[self.width*targety+targetx].on_enter(unit)
            self.observer.on_move_unit(x, y)

    def get_tile(self, x:int, y:int):
        return self.tiles[self.width*y+x]
   
    def get_effect(self, x:int, y:int):
        return self.effects[self.width*y+x]
    
    def get_unit(self, x:int, y:int):
        return self.units[self.width*y+x]

    def c_to_i(self, x, y):
        return self.width*y + x

    def is_space_empty(self, tiles:bool, x:int, y:int)->bool:
        return x>=0 and x<self.width and y>=0 and y<self.height \
            and not (self.tiles if tiles else self.units)[self.width*y+x]

    def tick(self, dt:float):
        for t in self.tiles:
            if t:
                t.tick(dt)
        for e in self.effects:
            if e:
                e.tick(dt)

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
