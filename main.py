import logging
import codecs
import sys
import os
import traceback

from grabber.manager.criteria import SearchCriteria
from grabber.manager.search_engine import TweetSearchEngine
from grabber.exporter.exporter import Exporter


def start_search(query, show_id, count=100, username=None, since=None, until=None, top_tweet=False):
    full_query = 'I rated %s #imdb' % query
    logging.info(full_query)
    criteria = SearchCriteria().set_query(full_query)

    if username is not None:
        criteria.setUsername(username)

    if since is not None:
        criteria.set_since(since)

    if until is not None:
        criteria.set_until(until)

    if top_tweet:
        criteria.setTopTweets(top_tweet)

    criteria.set_count(count)

    tweets = TweetSearchEngine.getTweets(criteria, show_id)
    exporter = Exporter()
    exporter.export_to_dat(tweets, query)
    exporter.close_files()


def get_shows():
    if not os.path.exists(os.path.abspath('dataset_output')):
        os.makedirs(os.path.abspath('dataset_output'))

    with codecs.open('dataset_input/input.txt', "a+") as input_file:
        input_file.seek(0)
        data = input_file.read()

    return [line.split('\n') for line in data.split('\n\n')]


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
    try:
        setup_logging()
        shows = get_shows()
        count = len(shows)
        for i in range(count):
            start_search(shows[i][1], shows[i][0])
            logging.info('%3d / %3d shows processed' % (i + 1, count))
    except:
        logging.error(traceback.extract_stack())


if __name__ == '__main__':
    main()
