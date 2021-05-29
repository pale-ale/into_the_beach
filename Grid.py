class TileBase:
    name = "-"

    def on_enter(self, unit):
        pass

    def on_damage(self, damage:int):
        pass


class TileForest(TileBase):
    name = "t"
    onfire = False

    def on_enter(self, unit):
        print("test")

    def on_damage(self, damage:int):
        self.onfire = True

class TileSea(TileBase):
    name = "~"
    onfire = False

    def on_enter(self, unit):
        assert isinstance(unit, UnitBase)
        if not unit.canswim:
            unit.drown()


class Grid:
    def __init__(self):
        self.height = 6
        self.width = 5
        self.tiles = [None]*self.width*self.height
        self.units = [None]*self.width*self.height

    def add_tile(self, x:int, y:int, tiletype:TileBase=TileBase):
        assert issubclass(tiletype, TileBase)
        newtile = tiletype()
        self.tiles[self.width*y+x] = newtile

    def add_unit(self,x,y):
        newunit = UnitBase(grid=self, name="rudolf")
        self.units[self.width*y+x] = newunit
        newunit.pos = [x, y]
            
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
            
    def is_space_empty(self, tiles:bool, x:int, y:int)->bool:
        return x>=0 and x<self.width and y>=0 and y<self.height \
            and not (self.tiles if tiles else self.units)[self.width*y+x]

    def show(self):
        text = ""
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[self.width*y+x]
                if tile:
                    text += tile.name
                else:
                    text += " "
            text += "\n"
        print(text)   


class UnitBase:
    
    def __init__(self, grid:Grid, name:str="p", hitpoints:int=5, canswim:bool=False):
        assert isinstance(grid, Grid)
        self.name = name
        self.hitpoints = hitpoints
        self.canswim = canswim
        self.grid = grid
        self.pos = [None, None]

    def drown(self):
        print("I drowned :(")
        self.grid.remove_unit(*self.pos)
    

grid = Grid()
grid2 = Grid()
userinputwhattodo = ""

grid.add_tile(2, 3, tiletype=TileForest)
grid.add_tile(2, 4, tiletype=TileSea)
grid.add_unit(2,3)
grid.move_unit(2,3,2,4)

print(grid.is_space_empty(True, 2, 3))
print(grid2.is_space_empty(True, 2, 3))
exit()

while userinputwhattodo != "x":
    grid.show()
    print("enter ...")
    userinputwhattodo = input()
    if userinputwhattodo == "new tile":
        print("insert x and y")
        userinputx = int(input())
        userinputy = int(input())
        grid.add_tile(userinputx,userinputy)
