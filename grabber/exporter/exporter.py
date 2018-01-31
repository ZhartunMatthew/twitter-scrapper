import codecs
import json

from grabber.models.tweet import Tweet

dialog_split = '[DIALOG-SPLIT]\n'
tweet_split = '\n'


def create_tweet_dump(tweets):
    with codecs.open('data/tweets/tweets.txt', 'w+', 'utf-8') as dump:
        [dump.write(json.dumps(tweet.to_dict(), ensure_ascii=False) + tweet_split) for tweet in tweets]


def restore_tweets():
    with codecs.open('data/tweets/tweets.txt', 'r+', 'utf-8') as dump:
        tweets = []
        file_data = dump.read()
        for tweet_string in file_data.split(tweet_split)[:-1]:
            tweet_json = json.loads(tweet_string)
            tweet = Tweet.from_dict(tweet_json)
            tweets.append(tweet)

        return tweets


def create_dialog_dump(dialogs):
    with codecs.open('data/dialogs/dialogs.txt', 'w+', 'utf-8') as dump:
        for dialog in dialogs:
            [dump.write(json.dumps(tweet.to_dict(), ensure_ascii=False) + tweet_split) for tweet in dialog]
            dump.write(dialog_split)


def restore_dialogs():
    with codecs.open('data/dialogs/dialogs.txt', 'r+', 'utf-8') as dump:
        dialogs = []
        file_data = dump.read()
        for dialog_string in file_data.split(dialog_split)[:-1]:
            dialog = []
            for tweet_string in dialog_string.split(tweet_split)[:-1]:
                print(tweet_string)
                tweet_json = json.loads(tweet_string)
                tweet = Tweet.from_dict(tweet_json)
                dialog.append(tweet)
            dialogs.append(dialog)

        return dialogs
