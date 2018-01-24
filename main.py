import logging
import datetime
import sys
import os

from grabber.search.search_engine import TweetSearchEngine
from grabber.search.criteria import SearchCriteria


def start_search(lang='ru', count=5000, result_type='recent', since='2017-01-01'):
    criteria = SearchCriteria()
    criteria = criteria \
        .set_lang(lang) \
        .set_count(count) \
        .set_result_type(result_type) \
        .set_since(since)

    search_engine = TweetSearchEngine()
    tweets = search_engine.get_tweets(criteria, backup_each=10)
    dialogs = search_engine.get_dialogs(tweets, backup_each=10)

    for dialog in dialogs:
        print('==================')
        for tweet in dialog:
            print(tweet)


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
    time_now = datetime.datetime.now
    logging.info('Start time: %s' % time_now().strftime("%Y-%m-%d %H:%M"))
    start_search(since=time_now().strftime("%Y-%m-%d"))
    logging.info('Start time: %s' % time_now().strftime("%Y-%m-%d %H:%M"))


if __name__ == '__main__':
    main()
