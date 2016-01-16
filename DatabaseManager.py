
from pymongo import MongoClient
from pymongo import cursor


class Database:
    """Database class is responsible for managing connection to database."""
    def __init__(self, server_addr='localhost', port=27017):
        self.client = MongoClient(server_addr, port)
        self.db = self.client.countrydb
        self.collection = self.db.countries
        self.cursor = cursor.Cursor(self.collection)

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

    def fetch_next_country_from_database(self):
        try:
            country = self.cursor.next()
            return country['name'], country['text'], country['flag']
        except StopIteration:
            return None

    def close(self):
        """Closes connection to database"""
        self.client.close()

if __name__ == '__main__':

    db = Database()
    for i in range(0, 14):
        print db.fetch_next_country_from_database()


