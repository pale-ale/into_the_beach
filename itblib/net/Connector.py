import socket
from typing import Optional
from itblib.Player import Player

class Connector():
    def __init__(self, authority:bool):
        self.authority = authority
        self.connection:Optional[socket.socket] = None
        self.acc_connection:Optional[socket.socket] = None

    def server_init(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setblocking(False)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind(('127.0.0.1', 13579))
        self.connection.listen(5)
    
    def get_incoming_connections(self):
        acceptedsockets = []
        while True:
            try:
                self.acc_connection, x = self.connection.accept()
                self.acc_connection.setblocking(False)
                acceptedsockets.append(self.acc_connection)
            except:
                return acceptedsockets

    def client_init(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(('127.0.0.1', 13579))
        self.connection.setblocking(False)
        self.acc_connection = self.connection
    
    def __del__(self):
        print("Tearing down connections.")
        try:
            if self.connection:
                self.connection.shutdown(0)
                self.connection.close()
            if self.acc_connection:
                self.acc_connection.shutdown(0)
                self.acc_connection.close()
        except:
            pass
    
    def send(self, prefix:str, content:str):
        assert len(prefix) <= 50, print(len(prefix))
        assert len(content) <= 1500, print(len(content))
        prefixdata = (prefix + '\0').ljust(50) .encode("utf8")
        contentdata = (content).ljust(1500).encode("utf8")
        if self.acc_connection:
            print("SND:", prefix, content)
            self.acc_connection.send(prefixdata + contentdata)
        else:
            print("I am not Connected!")
   
    def send_custom(self, connection:socket.socket, prefix:str, content:str):
        assert len(prefix) <= 50, print(len(prefix))
        assert len(content) <= 1500, print(len(content))
        prefixdata = (prefix + '\0').ljust(50) .encode("utf8")
        contentdata = (content).ljust(1500).encode("utf8")
        connection.send(prefixdata + contentdata)
    
    def send_to_clients(self, players:"dict[int, Player]", prefix:str, content:str):
        for player in players.values():
            self.send_custom(player.playersocket, prefix, content)

    def receive(self):
        if self.acc_connection:
            try:
                data = self.acc_connection.recv(1550)
                if data:
                    prefix, content = [d.strip() for d in data.decode("utf8").split('\0', 1) if d]
                    return prefix, content
            except BlockingIOError as bioe:
                return None
        else:
            print("I'm not connected to anything!")

    def receive_custom(self, playerconnection:socket.socket):
            if playerconnection:
                try:
                    data = playerconnection.recv(1550)
                    if data:
                        prefix, content = [d.strip() for d in data.decode("utf8").split('\0', 1) if d]
                        return prefix, content
                except BlockingIOError as bioe:
                    return None
            else:
                print("I'm not connected to anything!")
