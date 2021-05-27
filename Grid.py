class TileBase:
    name = "-"

    def on_enter(self):
        pass

    def on_damage(self, damage:int):
        pass


class TileForest(TileBase):
    name = "t"
    onfire = False

    def on_enter(self):
        print("test")

    def on_damage(self, damage:int):
        self.onfire = True


class Grid:
    width = 5
    height = 6
    tiles = [None]*width*height

    def add_tile(self, x:int, y:int):
        newtile = TileBase()
        self.tiles[self.width*x+y] = newtile

    def show(self):
        text = ""
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[self.width*y+x]
                if tile:
                    text += tile.name
                else:
                    text += "~"
            text += "\n"
        print(text)   


grid = Grid()
userinput = ""
while userinput != "x":
    grid.show()
    print("enter ...")
    userinput = input()
    if userinput == "w":
        grid.add_tile(2,2)
