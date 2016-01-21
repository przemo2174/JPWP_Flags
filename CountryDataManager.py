import re
import urllib2
from bs4 import BeautifulSoup


class CountryTextData:
    """CountryTextData class is responsible for managing, fetching and processing information about country."""
    __special_names = {
        'usa': ('united_states', 'united-states'),
        'russia': ('russian_federation', 'russian-federation')
    }

    def __init__(self, country_name):

        self.country_name = country_name.lower()
        self.__wiki_name, self.__flag_name = self.__get_wiki_flag_name()
        self.country_desc = '' # self.get_country_desc()
        self.flag_url = ''   # self.get_flag_url()

    def __get_wiki_flag_name(self):
        """Creates proper country name compatible with wikipedia and mapsworld

        Returns:
            A tuple containing proper wikipedia country name and mapsword name respectively

        """
        if self.country_name in CountryTextData.__special_names:
            return CountryTextData.__special_names[self.country_name]
        elif '_' in self.country_name:
            return self.country_name, self.country_name.replace('_', '-')
        else:
            return self.country_name, self.country_name

    def get_country_desc(self):
        """Fetches country description from wikipedia

        Returns:
            String containing country description

        """
        html = urllib2.urlopen('https://en.wikipedia.org/wiki/' + self.__wiki_name).read()
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')

        country_desc = ''
        for i in range(0, 5):
            country_desc += ''.join(paragraphs[i].find_all(text=True))

        text = ''.join(re.split('\[.*?\]', country_desc))  # building country description from paragraphs, erase ex. [12]
        text = re.sub(r'^(.|\n)*?(?=' + self.country_name[:4] + ')', '', text, 1, re.IGNORECASE)  # erase text until country_name is reached

        return text

    def get_flag_url(self):
        """Gets Flag URL corresponding to country

        Returns:
            String containing Flag URL

        """
        html = urllib2.urlopen('http://www.mapsofworld.com/flags/' + self.__flag_name + '-flag.html').read()
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            img_src = img_tag.get('src', None)
            if re.match('^http.+' + self.__flag_name + '.+|^\.\..+' + self.__flag_name + '.+', img_src):
                if img_src.startswith('..'):
                    img_src = 'http://www.mapsofworld.com/' + img_src[3:]
                return img_src

    @staticmethod
    def filter_text_with_tag(text, tag):  # returns list of sentences which contain word determined by tag value
        """Seeks in text in order to find all sentences containing word determined by tag
        Args:
            text(str): Text containing many sentences.
            tag(str): Word to be looked for in text

        Returns:
            List of sentences containing word determined by tag

        """
        sentences = re.split('[.?!]\s?(?=[A-Z])', text)
        lst = []
        for sentence in sentences:
            if re.search('\s' + tag + '(\s|,)', sentence):
                lst.append(sentence)
        return lst


