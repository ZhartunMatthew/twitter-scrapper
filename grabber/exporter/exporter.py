import codecs


def create_dump(tweets):
    with codecs.open('data/tweets/tweets.txt', 'w+', 'utf-8') as dump:
        [dump.write(str(tweet.to_dict()) + '\n') for tweet in tweets]


def create_dialog_dump(dialogs):
    with codecs.open('data/dialogs/dialogs.txt', 'w+', 'utf-8') as dump:
        for dialog in dialogs:
            dump.write('===================\n')
            [dump.write(str(tweet.to_dict()) + '\n') for tweet in dialog]

