import socket
import json


class ClientConnection:
    def __init__(self, client_ip_address='127.0.0.1', client_port=8000):
        self.ip_address = client_ip_address
        self.port = client_port
        self.country = ''
        self.type = 'text'
        self.json = {}

    def generate_request_json(self, country, tag=None, get_flag=False, check_flag=None):
        self.country = country
        request = 'country(%s)' % self.country
        if tag is not None:
            request += ';tag(%s)' % tag
        if get_flag:
            request += ';getflag'
            self.type = 'image'
        if check_flag is not None:
            request = 'checkflag(%s)' % check_flag

        self.json = {'address': self.ip_address, 'port': self.port, 'type': self.type, 'content': request}

    def send_json(self, server_ip_address, server_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip_address, server_port))
        mssg = json.dumps(self.json)
        sock.send(mssg)
        sock.close()

    def print_json(self):
        print json.dumps(self.json)

conn = ClientConnection()
conn.generate_request_json('Poland', get_flag=True)
conn.send_json('127.0.0.1', 8001)

