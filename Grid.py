from Tiles import TileBase
from Effects import EffectBase
from Units import UnitBase

class Grid:
    def __init__(self, width:int=10, height:int=10):
        self.height = width
        self.width = height
        self.tiles = [None]*width*height
        self.units = [None]*width*height
        self.effects = [None]*width*height

    def add_tile(self, x:int, y:int, tiletype:TileBase=TileBase):
        assert issubclass(tiletype, TileBase)
        newtile = tiletype()
        newtile.pos = [x,y]
        self.tiles[self.width*y+x] = newtile

    def add_effect(self, x:int, y:int, effecttype:EffectBase=EffectBase):
        assert issubclass(effecttype, EffectBase)
        neweffect = effecttype()
        neweffect.pos = [x,y]
        self.effects[self.width*y+x] = neweffect

    def add_unit(self, x, y, unittype:UnitBase=UnitBase):
        newunit = unittype(grid=self, name=" ")
        newunit.pos = [x, y]
        self.units[self.width*y+x] = newunit
            
    def remove_unit(self, x:int, y:int):
        if self.is_space_empty(False, x, y):
            print(f"error try to remove unit at {x} {y} which does not exist.")
            exit(1)
        self.units[self.width*y+x] = None
    
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
            print(unit.pos)

    def get_tile(self, x:int, y:int):
        return self.tiles[self.width*y+x]
   
    def get_effect(self, x:int, y:int):
        return self.effects[self.width*y+x]
    
    def get_unit(self, x:int, y:int):
        return self.units[self.width*y+x]

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
