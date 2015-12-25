import socket
import json
import requests


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
        elif get_flag:
            request += ';getflag'
            self.type = 'image'
        elif check_flag is not None:
            request += ';checkflag(%s)' % check_flag

        self.json = {'address': self.ip_address, 'port': self.port, 'type': self.type, 'content': request}

    def send_json(self, server_ip_address, server_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip_address, server_port))
        mssg = json.dumps(self.json)
        sock.send(mssg)
        while True:
            data = sock.recv(512)
            if len(data) < 1:
                break
            print data
        sock.close()

    def send_json_http(self, server_ip_address, server_port):
        url = 'http://%s:%s' % (server_ip_address, server_port)
        r = requests.post(url, json=self.json, timeout=10)
        print r.text

    def print_json(self):
        print json.dumps(self.json)


conn = ClientConnection()
conn.generate_request_json('russian_federation', check_flag="www.rosja.pl")
conn.send_json_http('127.0.0.1', 5000)

