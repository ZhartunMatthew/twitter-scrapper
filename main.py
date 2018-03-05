import logging
import datetime
import sys
import os
import time

from grabber.search.search_engine import TweetSearchEngine
from grabber.search.criteria import SearchCriteria


def start_search(lang='ru', count=100, batch_size=10, result_type='recent', since='2017-01-01'):
    criteria = SearchCriteria()
    criteria = criteria \
        .set_lang(lang) \
        .set_count(count) \
        .set_result_type(result_type) \
        .set_since(since)

    search_engine = TweetSearchEngine()
    tweets = search_engine.get_tweets(criteria, batch_size)
    dialogs = search_engine.get_dialogs(tweets, batch_size)


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


def main(index):
    logging.info('[%2d] Grabber started' % index)
    time_now = datetime.datetime.now
    start_search(since=time_now().strftime("%Y-%m-%d"), count=60000, batch_size=1000)
    logging.info('[%2d] Grabber ended' % index)


if __name__ == '__main__':
    setup_logging()
    for i in range(10):
        main(i)
        time.sleep(600)
