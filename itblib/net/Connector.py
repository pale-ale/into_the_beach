import socket
from typing import Optional
from itblib.Player import Player

class Connector():
    def __init__(self, authority:bool):
        self.authority = authority
        self.connection:Optional[socket.socket] = None
        self.acc_connection:Optional[socket.socket] = None
        self.RCV_PEEK_SIZE = 100
        self.SEPARATOR = '\0'
        self.PREAMBLE = self.SEPARATOR*1
        self.TERMINAL = self.SEPARATOR*2
        self.PREAMBLE_SIZE = len(self.PREAMBLE)
        self.TERMINAL_SIZE = len(self.TERMINAL)

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
    
    def send(self, connection:socket.socket, prefix:str, content:str):
        prefixdata = (prefix + self.PREAMBLE).encode("utf8")
        contentdata = (content + self.TERMINAL).encode("utf8")
        if connection:
            if len(content) > 100:
                print("Connector: SND:", prefix, content[:100] + "[...]")
            else:
                print("Connector: SND:", prefix, content)
            connection.send(prefixdata + contentdata)
        else:
            print("Connector: Invalid connection.")
    
    def send_client(self, prefix:str, content:str):
        self.send(self.acc_connection, prefix, content)
    
    def send_server_single(self, connection:socket.socket, prefix:str, content:str):
        self.send(connection, prefix, content)
    
    def send_server_all(self, players:"dict[int, Player]", prefix:str, content:str):
        for player in players.values():
            self.send_server_single(player.playersocket, prefix, content)

    def receive(self, connection:socket.socket):
        if connection:
            prefix = ""
            content = ""
            tmpdat = ""
            try:
                while len(prefix) == 0 or len(content) == 0:
                    peekdata = connection.recv(
                        self.RCV_PEEK_SIZE + max(self.PREAMBLE_SIZE, self.TERMINAL_SIZE), 
                        socket.MSG_PEEK
                    )
                    if len(peekdata) == 0:
                        return None
                    peekstr = peekdata.decode("utf-8")
                    preamble_index = peekstr.find(self.PREAMBLE)
                    terminal_index = peekstr.find(self.TERMINAL)
                    index = self.RCV_PEEK_SIZE - 1
                    if preamble_index >= 0:
                        index = preamble_index
                    if terminal_index >= 0 and terminal_index < preamble_index:
                        index = terminal_index
                    #if our message starts with a preamble or terminal separator, index is 0
                    if index == 0:
                        #i.e. we need to decide wether tmpdat is the preamble or content
                        if terminal_index == 0:
                            #note: the preamble is a substring of the terminal
                            content = tmpdat
                            connection.recv(self.TERMINAL_SIZE)
                            # remove the separators from the beginning
                        else:
                            prefix = tmpdat
                            connection.recv(self.PREAMBLE_SIZE)
                        tmpdat = ""
                    else:
                        tmpdat += connection.recv(index).decode("utf-8")
                return prefix, content
            except BlockingIOError as bioe:
                return None
            finally:
                pass
        print("Connector: Connection is invalid.")
    
    def receive_server(self, playerconnection:socket.socket):
        return self.receive(playerconnection)
    
    def receive_client(self):
        return self.receive(self.acc_connection)
