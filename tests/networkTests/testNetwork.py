import unittest

from itblib.net.Connector import Connector

class TestNetworkMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.server_connector = Connector(True)
        self.client_connector = Connector(False)
        self.server_connector.server_init()
        self.client_connector.client_connect()
        self.client_connections = self.server_connector.get_incoming_connections()
    
    def tearDown(self) -> None:
        del self.server_connector
        del self.client_connector

    def test_send_client_to_server(self):
        sendtext = ("Test", "C_to_S")
        self.client_connector.send_client(*sendtext)
        rcvtext = self.server_connector.receive_server(self.client_connections[0])
        self.assertEqual(sendtext, rcvtext)
    
    def test_send_server_to_client_single(self):
        sendtext = ("Test", "S_to_C")
        self.server_connector.send_server_single(self.client_connections[0], *sendtext)
        rcvtext = self.client_connector.receive_client()
        self.assertEqual(sendtext, rcvtext)
    
