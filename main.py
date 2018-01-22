import logging
import codecs
import sys
import os
import traceback

from grabber.manager.criteria import SearchCriteria
from grabber.manager.search_engine import TweetSearchEngine
from grabber.exporter.exporter import Exporter


def start_search(lang='en', count=100, result_type='popular', since='2017-01-01', until='2017-12-31'):
    criteria = SearchCriteria()
    criteria = criteria\
        .set_lang(lang)\
        .set_count(count)\
        .set_result_type(result_type)\
        .set_since(since)\
        .set_until(until)

    tweets = TweetSearchEngine.getTweets(criteria)
    # TODO: Exporter work
    # exporter = Exporter()


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    fh = logging.FileHandler(os.path.abspath('grabber.log'))
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    root.addHandler(fh)


def main():
    setup_logging()
    logging.info('Grabber started')
    # try:
    start_search()
    # except Exception as ex:
    #     logging.error(ex)


if __name__ == '__main__':
    main()
