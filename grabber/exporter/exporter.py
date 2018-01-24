
import codecs

from datetime import datetime


def create_dump(tweets):
    with codecs.open('data/tweets/tweets_%s.txt' % datetime.now().strftime("%Y-%m-%d %H+%M"), 'w+', 'utf-8') as dump:
        [dump.write(str(tweet.to_dict()) + '\n') for tweet in tweets]


def create_dialog_dump(dialogs):
    with codecs.open('data/dialogs/dialogs_%s.txt' % datetime.now().strftime("%Y-%m-%d %H+%M"), 'w+', 'utf-8') as dump:
        dump.write('[')
        for i, dialog in enumerate(dialogs):
            dump.write('[')
            for j, tweet in enumerate(dialog):
                dump.write(str(tweet.to_dict() + '\n'))
            dump.write(']\n')
        dump.write(']')
