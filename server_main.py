import json
from itblib.net.Connector import Connector

c = Connector(True)
c.server_init()

prefix = "MapTransfer"
data = "MapGrasslands"
#c.send(prefix, data)

with open("itblib/maps/sea_map.json","r") as f:
    contents = f.read()
obj = json.loads(contents)
contents = json.dumps(obj)
c.send(prefix, contents)
