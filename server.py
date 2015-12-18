
import socket
import json


class Server:
    def __init__(self):
        pass

    def get_json(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 8001))
        sock.listen(5)
        print 'Listening...'
        c, ddr = sock.accept()
        while True:
            data = c.recv(512)
            if len(data) < 1:
                break
            print data
        sock.close()

server = Server()
server.get_json()
