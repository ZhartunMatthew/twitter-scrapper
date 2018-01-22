import re


class TweetUtil:

    def __init__(self):
        """
        Using for extract data from tweet
        """
        pass

    @staticmethod
    def extract_title(text):
        """
        Extracting title from tweet text
        :param text: Tweet content
        :return: Show title
        """
        pattern = '(?<=I rated )(.*)(?=([0-9]+)/10)'
        txt = TweetUtil.__extract_by_pattern(text, pattern)
        if len(txt) > 1:
            txt = txt[0]
        else:
            return ''

        return txt

    @staticmethod
    def extract_rating(text):
        """
        Extracting rating from tweet text
        :param text: Tweet content
        :return: Show rating
        """
        pattern = '([0-9]+)/10'
        return TweetUtil.__extract_by_pattern(text, pattern)

    @staticmethod
    def __extract_by_pattern(text, pattern):
        p = re.compile(pattern, re.M | re.I)
        matches = p.findall(text)
        if len(matches) != 0:
            match = matches[0]
        else:
            match = ''
        return match

    @staticmethod
    def get_imdb_id(imdb_link):
        """
        Extracting rating from imdb link
        :param imdb_link: Show link to imdb like http://www.imdb.com/title/tt0970866
        :return: Show rating
        """
        pattern = '.*?/tt([0-9]*)/*$'
        p = re.compile(pattern, re.M | re.I)

        matches = p.findall(imdb_link)
        if len(matches) > 0:
            return matches[0]
        else:
            return -1
