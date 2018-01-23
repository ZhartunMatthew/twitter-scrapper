import codecs

from datetime import datetime


def create_dump(tweets):
    with codecs.open('data/dump_tweets_%s.txt' % datetime.now().strftime("%Y-%m-%d %H+%M"), 'w+', 'utf-8') as dump:
        [dump.write(str(tweet.to_dict()) + '\n') for tweet in tweets]
