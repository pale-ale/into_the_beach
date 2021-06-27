from itblib.net.Connector import Connector

c = Connector(True)
c.server_init()

prefix = "MapTransfer"
data = "MapGrasslands"
c.send(prefix, data)
