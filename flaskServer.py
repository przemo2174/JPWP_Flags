from flask import Flask, request
from CountryDataManager import CountryTextData
from DatabaseManager import Database
import re
import json
from ImageComparer import ImageComparer
import os


class Server:
    def __init__(self):
        self.db = Database()
        self.country_name = None
        self.tag_value = None
        self.checkflag_value = None
        self.content = ''

    def get_and_process_json_from_client(self):
        json_dict = request.get_json()
        self.content = json_dict['content'].split(';')

        try:  # check if country_name is in json
            self.country_name = re.search('^.+\((.+)\).*?', self.content[0]).group(1)  # get country name from json
        except AttributeError:
            self.country_name = ''
        self.tag_value = Server.__retrieve_json_attribute_value('tag', self.content)
        self.checkflag_value = Server.__retrieve_json_attribute_value('checkflag', self.content)

    def generate_and_return_response(self):
        if self.checkflag_value:
            name = self.check_flag()
            delete_all_images()
            self.db.close()
            return name
        else:
            country_info = CountryTextData(self.country_name)
            print 'success'

            _, description, flag_url = self.try_get_data_from_database(country_info)
            self.db.close()

            if 'getflag' in self.content:
                return flag_url
            elif self.tag_value:
                return json.dumps(CountryTextData.filter_text_with_tag(description, self.tag_value))
            else:
                return description

    def try_get_data_from_database(self, country_info):
        country_name = country_info.country_name
        country_tuple = self.db.get_country_from_database(country_name)

        if country_tuple is None:  # if requesting country is not found in database, fetch data from internet
            description = country_info.get_country_desc()
            flag_url = country_info.get_flag_url()
            self.db.add_country_to_database(country_name, description, flag_url)
            print 'from internet'
        else:
            _, description, flag_url = self.db.get_country_from_database(country_name)
            print 'from database'
        return country_name, description, flag_url

    def check_flag(self):
        file_name_unk = ImageComparer.download_image(self.checkflag_value, 'mysterious')
        max_res = 0
        country_name = ''
        while True:
            country = self.db.fetch_next_country_from_database()
            if country is not None:
                name, text, flag_url = country
                try:
                    file_name_co = ImageComparer.download_image(flag_url, name)
                except ValueError:
                    continue
                res = ImageComparer.compare_images(file_name_unk, file_name_co)
                print name
                if res > max_res:
                    max_res = res
                    country_name = name
            else:
                break
        return country_name

    @staticmethod
    def __retrieve_json_attribute_value(data, content):
        if data == 'tag' or data == 'checkflag':
            tag = ''.join([x for x in content if data in x])  # if there is no tag in json, tag variable will be empty
            if tag:  # check if json has tag and retrieve it
                return tag[tag.find('(')+1:-1]  # retrieve tag value
            else:
                return None
        else:
            return None


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    server = Server()
    server.get_and_process_json_from_client()
    return server.generate_and_return_response()


def delete_all_images():
    file_list = [file for file in os.listdir('.') if file.endswith('png') or file.endswith('jpg')]
    for file in file_list:
        os.remove(file)


if __name__ == '__main__':
    app.run(debug=True)
