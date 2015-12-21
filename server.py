import CountryDataManager
import socket
import json


class Server:
    def __init__(self):
        self.country_info = None

    def get_json(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 8002))
        sock.listen(5)
        print 'Listening...'
        c, ddr = sock.accept()
        while True:
            data = c.recv(1024)
            if not data:
                break
            print data
        dictionary = json.loads(data)
        content = dictionary['content']
        print content
        #c.send(self.country_info.flag_url)
        c.close()
        sock.close()

server = Server()
server.get_json()
