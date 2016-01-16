from flask import Flask, request
from CountryDataManager import CountryTextData
from DatabaseManager import Database
import re
import json
from ImageComparer import ImageComparer
import os


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
        json_dict = request.get_json()
        content = json_dict['content'].split(';')

        try:  # check if country_name is in json
            country_name = re.search('^.+\((.+)\).*?', content[0]).group(1)  # get country name from json
        except AttributeError:
            country_name = ''

        tag_value = retrieve_json_attribute_value('tag', content)
        checkflag_value = retrieve_json_attribute_value('checkflag', content)
        db = Database()

        if checkflag_value:
            name = check_flag(checkflag_value, db)
            delete_all_images()
            return name
        else:
            country_info = CountryTextData(country_name)
            print 'success'

            _, description, flag_url = try_get_from_database(country_info, db)
            db.close()

            if 'getflag' in content:
                return flag_url
            elif tag_value:
                return json.dumps(CountryTextData.filter_text_with_tag(description, tag_value))
            else:
                return description


def try_get_from_database(country_info, db):
    country_name = country_info.country_name
    country_tuple = db.get_country_from_database(country_name)

    if country_tuple is None:  # if requesting country is not found in database, fetch data from internet
        description = country_info.get_country_desc()
        flag_url = country_info.get_flag_url()
        db.add_country_to_database(country_name, description, flag_url)
        print 'from internet'
    else:
        _, description, flag_url = db.get_country_from_database(country_name)
        print 'from database'
    return country_name, description, flag_url


def retrieve_json_attribute_value(data, content):
    if data == 'tag' or data == 'checkflag':
        tag = ''.join([x for x in content if data in x])  # if there is no tag in json, tag variable will be empty
        if tag:  # check if json has tag and retrieve it
            return tag[tag.find('(')+1:len(tag) - 1]  # retrieve tag value
        else:
            return None
    else:
        return None


def check_flag(url, db):
    file_name_unk = ImageComparer.download_image(url, 'unknown_country')
    max_res = 0
    country_name = ''
    while True:
        country = db.fetch_next_country_from_database()
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


def delete_all_images():
    file_list = [file for file in os.listdir('.') if file.endswith('png') or file.endswith('jpg')]
    for file in file_list:
        os.remove(file)


@app.route('/profile/<username>')
def profile(username):
    return 'Hi %s' % username


if __name__ == '__main__':
    app.run(debug=True)
    db = Database()
    check_flag('http://www.mapsofworld.com/images/world-countries-flags/austria-flag.gif', db)
    db.close()
