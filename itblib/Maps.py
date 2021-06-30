import json

class Map:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.tileids = [None]*self.width*self.height
        self.unitids = [None]*self.width*self.height
        self.effectids = [None]*self.width*self.height
    
    def import_from_str(self, importstr):
        data = json.loads(importstr)
        self.width = data["width"]
        self.height = data["height"]
        self.tileids = data["tileids"]
        self.unitids = data["unitids"]
        self.effectids = data["effectids"]
    
    def export_to_str(self):
        data = {"width": self.width,
                "height": self.height,
                "tileids": self.tileids,
                "unitids": self.unitids,
                "effectids": self.effectids,
                }
        jsonstr = json.dumps(data)
        return jsonstr

    def iterate_tiles(self):
        print(self.height)
        for y in range(self.height):
            for x in range(self.width):
                yield x,\
                    y,\
                    self.tileids[y*self.width+x],\
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
        self.unitids[30] = 0
        self.unitids[31] = 1
        self.unitids[96] = 0
        self.unitids[55] = 2
       