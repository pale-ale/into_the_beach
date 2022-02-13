import unittest

from itblib.Game import Session
from itblib.Grid import Grid
from itblib.net.Connector import Connector


class TestJoinGameMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.server_connector = Connector(True)
        self.server_session = Session(self.server_connector)
        self.server_grid = Grid(self.server_connector, width=3, height=3)
        self.client_connector = Connector(False)
        self.client_session = Session(self.client_connector)
        self.client_grid = Grid(self.client_connector, width=2, height=3)
        
        self.server_connector.server_init()
        self.client_connector.client_connect()
        self.server_client_connections = self.server_connector.get_incoming_connections()
        self.assertGreater(len(self.server_client_connections), 0)
    
    def test_playerinfo_transfer(self):
        pass
        #this cannot be tested properly, due to NetEvents being a singleton.
        # TODO: run 2 seperate scripts, so we get 2 seperate NetEvents
            
    
    
