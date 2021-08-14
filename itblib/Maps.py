import json

class Map:
    """Contains only serializable information, e.g. it's dimensions, unit|tile|effect-ids and so forth."""

    def __init__(self):
        self.width = 10
        self.height = 10
        self.tileids:"list[int|None]" = [None]*self.width*self.height
        self.unitids:"list[int|None]" = [None]*self.width*self.height
        self.effectids:"list[list[int]]" = [[] for i in range(self.width*self.height)]
    
    def import_from_str(self, importstr):
        """Deserialize a json-str and update the data accordingly."""
        data = json.loads(importstr)
        self.width = data["width"]
        self.height = data["height"]
        self.tileids = data["tileids"]
        self.unitids = data["unitids"]
        self.effectids = data["effectids"]
    
    def export_to_str(self):
        """Serialize the contained data into a json-str."""
        data = {"width": self.width,
                "height": self.height,
                "tileids": self.tileids,
                "unitids": self.unitids,
                "effectids": self.effectids,
                }
        jsonstr = json.dumps(data)
        return jsonstr

    def iterate_tiles(self):
        """Return a generator for easy access, iterating every space once and yielding the units, tiles and effects on it."""
        for y in range(self.height):
            for x in range(self.width):
                yield (x,y),\
                    self.tileids[y*self.width+x],\
                    self.effectids[y*self.width+x],\
                    self.unitids[y*self.width+x]

class MapGrasslands(Map):
    """A map currently used for testing."""
    
    def __init__(self):
        super().__init__()
        for x in range(0, 100):
            self.tileids[x] = 1
        for x in range (0, 5):
            self.tileids[x] = 5
        for x in range (10, 15):
            self.tileids[x] = 5
        for x in range (20, 25):
            self.tileids[x] = 5
        for x in range (30, 35):
            self.tileids[x] = 5
        for x in range (40, 45):
            self.tileids[x] = 5
        
        for x in range(5, 10):
            self.tileids[x] = 2
        for x in range(15, 20):
            self.tileids[x] = 2
        for x in range(25, 30):
            self.tileids[x] = 2
        for x in range(35, 40):
            self.tileids[x] = 2
        for x in range(45, 50):
            self.tileids[x] = 2
        
        for x in range (55, 60):
            self.tileids[x] = 5
        for x in range (65, 70):
            self.tileids[x] = 5
        for x in range (75, 80):
            self.tileids[x] = 5
        for x in range (85, 90):
            self.tileids[x] = 5
        for x in range (95, 100):
            self.tileids[x] = 5

        for x in range (50, 55):
            self.tileids[x] = 2
        for x in range (60, 65):
            self.tileids[x] = 2
        for x in range (70, 75):
            self.tileids[x] = 2
        for x in range (80, 85):
            self.tileids[x] = 2
        for x in range (90, 95):
            self.tileids[x] = 2
        for x in range(0, 10):
            self.effectids[x].append(2+int(x/2))    
        for x in range(75, 78):
            self.effectids[x].append(5)
        wheat = [57, 67, 22, 23, 24, 32, 42, 34, 44, 55, 56, 65, 43, 33, 66]
        for x in wheat:
            self.effectids[x].append(5)
        