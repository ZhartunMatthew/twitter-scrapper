import logging
import datetime
import sys
import os

from grabber.search.search_engine import TweetSearchEngine
from grabber.search.criteria import SearchCriteria
from grabber.exporter.exporter import Exporter


def start_search(lang='ru', count=20, result_type='recent', since='2017-01-01'):
    criteria = SearchCriteria()
    criteria = criteria \
        .set_lang(lang) \
        .set_count(count) \
        .set_result_type(result_type) \
        .set_since(since)

    tweets = TweetSearchEngine.get_tweets(criteria)
    for tweet in tweets:
        print(tweet)
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
    now = datetime.datetime.now()
    start_search(since=now.strftime("%Y-%m-%d"))


if __name__ == '__main__':
    main()
