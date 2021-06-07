class Map:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.tileids = [None]*self.width*self.height
        self.unitids = [None]*self.width*self.height
        self.effectids = [None]*self.width*self.height

    def iterate_tiles(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x,y,self.tileids[y*self.width+x],\
                    self.effectids[y*self.width+x],\
                    self.unitids[y*self.width+x]

class MapGrasslands(Map):
    def __init__(self):
        super().__init__()
        for x in range(0, 88):
            self.tileids[x] = 1
        for x in range(75, self.width*self.height):
            self.tileids[x] = 0
        for x in range(0, 64):
            self.effectids[x] = 0
        for x in range(2, 8):
            self.effectids[x] = 1
        for x in range(13, 16):
            self.effectids[x] = 1
        self.unitids[94] = 0
        self.unitids[95] = 0
        self.unitids[96] = 0
       