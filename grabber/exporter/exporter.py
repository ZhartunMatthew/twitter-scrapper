import json
import codecs


def create_tweet_dump(tweets):
    with codecs.open('data/tweets/tweets.txt', 'w+', 'utf-8') as dump:
        [dump.write(json.dumps(tweet.to_dict(), ensure_ascii=False) + '\n') for tweet in tweets]


def restore_tweet_dump():
    with codecs.open('data/tweets/tweets.txt', 'r', 'utf-8') as dump:
        pass


def create_dialog_dump(dialogs):
    with codecs.open('data/dialogs/dialogs.txt', 'w+', 'utf-8') as dump:
        for dialog in dialogs:
            dump.write('===================\n')
            [dump.write(str(tweet.to_dict()) + '\n') for tweet in dialog]

