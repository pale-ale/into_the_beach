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
        for x in range(0, 88):
            self.tileids[x] = 2
        for x in range(75, self.width*self.height):
            self.tileids[x] = 1
        for x in range(3):
            self.tileids[x+85] = 5
            self.tileids[x+95] = 5
        for x in range(3, 6):
            self.tileids[x] = 4
        for x in range(74, 78):
            self.effectids[x].append(5)
    