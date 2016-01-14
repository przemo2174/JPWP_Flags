
from pymongo import MongoClient


class Database:
    """Database class is responsible for managing connection to database."""
    def __init__(self, server_addr='localhost', port=27017):
        self.client = MongoClient(server_addr, port)
        self.db = self.client.countrydb
        self.collection = self.db.countries

    def get_country_from_database(self, country_name):  # if found, return a tuple containing all country info
        """Tries to find information corresponding to given country in database.

        Args:
            country_name: Country name for which information should be fetched.

        Returns:
            A tuple containing country name, country description and country flag URL.
            When country is not found in database, it returns None.

        """
        country = self.collection.find_one({"name": country_name})
        if country is not None:
            return country['name'], country['text'], country['flag']
        else:
            return None

    def add_country_to_database(self, country_name, country_text, country_flag):
        """"Adds country information to database.

        Args:
            country_name: Country name.
            country_text: Country description.
            country_flag: Country flag URL

        """
        self.collection.insert_one(
            {
                "name": country_name,
                "text": country_text,
                "flag": country_flag
            }
        )

    def fetch_all_countries_from_database(self):
        pass




    def close(self):
        """Closes connection to database"""
        self.client.close()

if __name__ == '__main__':

    db = Database()
    db.add_country_to_database('argentina', 'nice country', 'www')
    data = db.get_country_from_database('argentina')
    if data:
        print data[1]
    else:
        print "no"


