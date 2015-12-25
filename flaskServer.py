from flask import Flask, request
from CountryDataManager import CountryTextData
from DatabaseManager import Database
import re
import json
from ImageComparer import ImageComparer


app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
        json_dict = request.get_json()
        content = json_dict['content'].split(';')

        country_name = re.search('^.+\((.+)\).*?', content[0]).group(1)  # get country name from json
        country_info = CountryTextData(country_name)

        print 'success'

        tag_value = retrieve_json_attribute_value('tag', content)
        checkflag_value = retrieve_json_attribute_value('checkflag', content)

        db = Database()
        print country_name
        country_tuple = db.get_country_from_database(country_name)
        if country_tuple is None:  # if requesting country is not found in database
            description = country_info.get_country_desc()
            flag_url = country_info.get_flag_url()
            db.add_country_to_database(country_info.country_name, description, flag_url)
            print 'from internet'
        else:
            name, description, flag_url = db.get_country_from_database(country_name)
            print 'from database'
        db.close()

        if 'getflag' in content:
            return flag_url
        elif tag_value:
            return json.dumps(CountryTextData.filter_text_with_tag(description, tag_value))
        elif checkflag_value:
            print checkflag_value
            print flag_url
            ImageComparer.download_image(flag_url, country_name + '.gif')
            return 'some country'
        else:
            return description


def retrieve_json_attribute_value(data, content):
    if data == 'tag' or data == 'checkflag':
        tag = ''.join([x for x in content if data in x])  # if there is no tag in json, tag variable will be empty
        if tag:  # check if json has tag and retrieve it
            return tag[tag.find('(')+1:len(tag) - 1]  # retrieve tag value
        else:
            return None
    else:
        return None


@app.route('/profile/<username>')
def profile(username):
    return 'Hi %s' % username


if __name__ == '__main__':
    app.run(debug=True)
