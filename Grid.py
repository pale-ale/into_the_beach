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
        self.tiles[self.width*y+x] = newtile

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


class PlayerGrid:
    width = Grid.width
    height = Grid.height
    player= [None]*width*height

    def add_player(self,x,y):
        newplayer = Player()
        self.player[self.width*y+x] = newplayer
    
    def move_player(self, x, y, dx, dy):
        if dx != 0 or dy != 0:
            self.player[self.width*(y+dy)+(x+dx)] = self.player[self.width*y+x]
            self.player[self.width*y+x] = None
    
    def show(self):
        text = ""
        for x in range(self.width):
            for y in range(self.height):
                player = self.player[self.width*y+x]
                if player:
                    text += player.name
                else:
                    text += "_"
            text += "\n"
        print(text)   


class Player:
    name = "p"
    hitpoints = 5


grid = Grid()
playergrid =PlayerGrid()
userinputwhattodo = ""
while userinputwhattodo != "x":
    grid.show()
    playergrid.show()
    print("enter ...")
    userinputwhattodo = input()
    if userinputwhattodo == "new tile":
        print("insert x and y")
        userinputx = int(input())
        userinputy = int(input())
        grid.add_tile(userinputx,userinputy)
    if userinputwhattodo == "new player":
        print("insert x and y")
        userinputx = int(input())
        userinputy = int(input())
        playergrid.add_player(userinputx,userinputy)
    if userinputwhattodo == "move player":
        print("insert x and y and dx and dy")
        userinputx = int(input())
        userinputy = int(input())
        userinputdx = int(input())
        userinputdy = int(input())
        playergrid.move_player(userinputx,userinputy,userinputdx,userinputdy)
