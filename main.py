from itblib.Grid import Grid
from itblib.Maps import MapGrasslands

g = Grid(None, None)
g2 = Grid(None, None)
m = MapGrasslands()
g.load_map(m, False)

d = g.extract_data(["width", "height", "phasetime", "tiles"])
print(d)
g2.insert_data(d)
g.show()
g2.show()