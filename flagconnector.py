import re
import urllib2
from bs4 import BeautifulSoup


class CountryTextData:
    __special_names = {'usa': ('united_states', 'united-states'),
                        'russia': ('russian_federation', 'russian-federation')}

    def __init__(self, country_name):

        self.country_name = country_name.lower()
        self.__wiki_name, self.__flag_name = self.__get_wiki_flag_name()
        self.country_desc = self.__get_country_desc()
        self.flag_url = self.__get_flag_url()

    def __get_wiki_flag_name(self):
        if self.country_name in CountryTextData.__special_names:
            return CountryTextData.__special_names[self.country_name]
        else:
            return self.country_name, self.country_name

    def __get_country_desc(self):
        html = urllib2.urlopen('https://en.wikipedia.org/wiki/' + self.__wiki_name).read()
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')

        if not re.match('.*' + self.country_name + '.*', str(paragraphs[0]), re.IGNORECASE):
            del paragraphs[0]

        country_desc = ''

        for i in range(0, 5):
            country_desc += ''.join(paragraphs[i].find_all(text=True))

        return ''.join(re.split('\[.*?\]', country_desc))

    def __get_flag_url(self):
        html = urllib2.urlopen('http://www.mapsofworld.com/flags/' + self.__flag_name + '-flag.html').read()
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            img_src = img_tag.get('src', None)
            if re.match('^http.+' + self.__flag_name + '.+|^\.\..+' + self.__flag_name + '.+', img_src):
                if img_src.startswith('..'):
                    img_src = 'http://www.mapsofworld.com/' + img_src[3:]
                return img_src






country = CountryTextData('usa')
print country.country_desc
print country.flag_url
