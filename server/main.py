import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', 13579))
    s.listen(5)
    a_s, x = s.accept()

    print( a_s.recv(1000).decode(encoding="utf8"))
