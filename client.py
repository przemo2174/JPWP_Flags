import socket
import json
import requests
from ImageComparer import ImageComparer


class ClientConnection:
    """ClientConnection class is responsible for creating and sending requests to server and receiving responses"""
    def __init__(self, server_ip_address='127.0.0.1', server_port=5000):
        """Creates ClientConnection object

        Args:
            server_ip_address: IPv4 address to connect
            server_port: Port to connect

        """
        self.ip_address = server_ip_address
        self.port = server_port
        self.country = ''
        self.type = 'text'
        self.json = {}

    def generate_request_json(self, country='', tag=None, get_flag=False, check_flag=None):
        """Generates json based on given arguments
        Examples:
            generate_request_json('france') - returns description of france
            generate_request_json('germany', tag='with') - returns sentences from germany description containing 'with' word.
            generate_request_json('england', get_flag=True) - returns URL of england flag.
            generate_request_json(checkflag='[flag_url]') - returns country name corresponding to flag.

        Args:
            country(str): Country name
            tag(str): Special tag which equals to some string. If it is given, server returns all sentences which
            contain word determined by this tag, otherwise all sentences describing country are returned.
            get_flag(bool): When True, server returns flag URL corresponding to given country.
            check_flag(str): Contains URL of unknown flag. When this argument is given it should be only argument passed
            to this function

        """
        self.country = country
        request = 'country(%s)' % self.country
        if tag is not None:
            request += ';tag(%s)' % tag
        elif get_flag:
            request += ';getflag'
            self.type = 'image'
        elif check_flag is not None:
            request = 'checkflag(%s)' % check_flag

        self.json = {'address': self.ip_address, 'port': self.port, 'type': self.type, 'content': request}

    def send_json_http(self):
        """Send json to server using POST method"""

        url = 'http://%s:%s' % (self.ip_address, self.port)
        r = requests.post(url, json=self.json, timeout=30)
        return r.text

    def print_json(self):
        """Prints json string"""
        print json.dumps(self.json)


conn = ClientConnection('127.0.0.1', 5000)
conn.generate_request_json(check_flag='http://www.mapsofworld.com/images/world-countries-flags/finland-flag.gif')
print conn.json
response = conn.send_json_http()
print response


