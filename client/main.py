import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("nani?")
    s.connect(('127.0.0.1', 13579))

    s.send("Hello".encode("utf8"))
