
from pymongo import MongoClient


class Database:
    def __init__(self, server_addr='localhost', port=27017):
        self.client = MongoClient(server_addr, port)
        self.db = self.client.countrydb
        self.collection = self.db.countries

    def get_country_from_database(self, country_name):  # if found, return a tuple containing all country info
        country = self.collection.find_one({"name": country_name})
        if country is not None:
            return country['name'], country['text'], country['flag']
        else:
            return None

    def add_country_to_database(self, country_name, country_text, country_flag):
        self.collection.insert_one(
            {
                "name": country_name,
                "text": country_text,
                "flag": country_flag
            }
        )

    def close(self):
        self.client.close()

if __name__ == '__main__':

    db = Database()
    db.add_country_to_database('argentina', 'nice country', 'www')
    data = db.get_country_from_database('argentina')
    if data:
        print data[1]
    else:
        print "no"


