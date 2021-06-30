import socket

class Connector():
    def __init__(self, authority:bool):
        self.authority = authority
        self.connection = None
        self.acc_connection = None

    def server_init(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_NONBLOCK)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection.bind(('127.0.0.1', 13579))
        self.connection.listen(5)
    
    def get_incoming_connections(self):
        acceptedsockets = []
        while True:
            try:
                self.acc_connection, x = self.connection.accept()
                acceptedsockets.append(self.acc_connection)
            except:
                return acceptedsockets

    def client_init(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(('127.0.0.1', 13579))
        self.acc_connection = self.connection
    
    def __del__(self):
        print("Tearing down connections.")
        if self.connection:
            self.connection.shutdown(0)
            self.connection.close()
        if self.acc_connection:
            self.acc_connection.shutdown(0)
            self.acc_connection.close()
    
    def send(self, prefix:str, content:str):
        prefixdata = (prefix + '\0').encode("utf8")
        contentdata = (content + '\0').encode("utf8")
        assert len(prefixdata) <= 50, print(len(prefixdata))
        assert len(contentdata) <= 1500, print(len(contentdata))
        if self.acc_connection:
            self.acc_connection.send(prefixdata + contentdata)
   
    def send_custom(self, connection, prefix:str, content:str):
        prefixdata = (prefix + '\0').encode("utf8")
        contentdata = (content + '\0').encode("utf8")
        assert len(prefixdata) <= 50, print(len(prefixdata))
        assert len(contentdata) <= 1500, print(len(contentdata))
        connection.send(prefixdata + contentdata)

    def receive(self):
        if self.acc_connection:
            data = self.acc_connection.recv(1550)
            if data:
                prefix, content = [d for d in data.decode("utf8").split('\0') if d]
                return prefix, content