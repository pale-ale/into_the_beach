import json

class Map:
    """Contains only serializable information, e.g. it's dimensions, unit|tile|effect-ids and so forth."""

    def __init__(self):
        self.width = 10
        self.height = 10
        self.tileids:"list[int|None]" = [None]*self.width*self.height
        self.unitids:"list[int|None]" = [None]*self.width*self.height
        self.tileeffectids:"list[list[int]]" = [[] for i in range(self.width*self.height)]
        self.uniteffectids:"list[list[int]]" = [[] for i in range(self.width*self.height)]
    
    def import_from_str(self, importstr):
        """Deserialize a json-str and update the data accordingly."""
        data = json.loads(importstr)
        self.width = data["width"]
        self.height = data["height"]
        self.tileids = data["tileids"]
        self.unitids = data["unitids"]
        self.tileeffectids = data["tileeffectids"]
        self.uniteffectids = data["uniteffectids"]
    
    def export_to_str(self):
        """Serialize the contained data into a json-str."""
        data = {"width": self.width,
                "height": self.height,
                "tileids": self.tileids,
                "unitids": self.unitids,
                "tileeffectids": self.tileeffectids,
                "uniteffectids": self.uniteffectids,
                }
        jsonstr = json.dumps(data)
        return jsonstr

    def iterate_tiles(self):
        """Return a generator for easy access, iterating every space once and yielding the units, tiles and effects on it."""
        for y in range(self.height):
            for x in range(self.width):
                yield (x,y),\
                    self.tileids[y*self.width+x],\
                    self.tileeffectids[y*self.width+x],\
                    self.uniteffectids[y*self.width+x],\
                    self.unitids[y*self.width+x]

class MapGrasslands(Map):
    """A map currently used for testing."""
    
    def __init__(self):
        super().__init__()
        for x in range(0, 100):
            self.tileids[x] = 1
        self.tileids[41] = 2
        self.tileids[42] = 2
        self.tileids[51] = 4
        self.tileids[52] = 4
        self.tileids[44] = 3
        self.tileids[45] = 3
        self.tileids[54] = 3
        self.tileids[55] = 3
        self.tileids[47] = 4
        self.tileids[48] = 4
        self.tileids[57] = 2
        self.tileids[58] = 2
        mountain = [9, 19, 8, 80, 90, 91]
        for x in mountain:
            self.tileeffectids[x].append(3)
        self.tileeffectids[9].append(3)
        town = [14, 15, 24, 25, 74, 75, 84, 85]
        for x in town:
            self.tileeffectids[x].append(6)
        wheat = [0, 1, 10]
        for x in wheat:
            self.tileeffectids[x].append(5)
        river = [61, 62, 37, 38]
        for x in river:
            self.tileeffectids[x].append(4)  
        self.tileeffectids[11].append(7)
        self.tileeffectids[89].append(7)
        self.tileeffectids[33].append(2)
        self.tileeffectids[66].append(2)
        self.tileeffectids[36].append(2)
        self.tileeffectids[63].append(2)

