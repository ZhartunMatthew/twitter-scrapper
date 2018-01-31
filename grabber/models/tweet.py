class Tweet:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.user_name = None
        self.text = None
        self.time = None
        self.reply_to_tweet = None
        self.reply_to_user = None
        self.reply_to_link = None

    @staticmethod
    def from_dict(tweet_dict):
        tweet = Tweet()
        tweet.id = tweet_dict.get('id', None)
        tweet.user_id = tweet_dict.get('user_id', None)
        tweet.user_name = tweet_dict.get('user_name', None)
        tweet.text = tweet_dict.get('text', None)
        tweet.time = tweet_dict.get('time', None)
        tweet.reply_to_tweet = tweet_dict.get('reply_to_tweet', None)
        tweet.reply_to_user = tweet_dict.get('reply_to_user', None)
        tweet.reply_to_link = tweet_dict.get('reply_to_link', None)
        return tweet

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'user_name': self.user_name,
                'text': self.text,
                'time': self.time,
                'reply_to_tweet': self.reply_to_tweet,
                'reply_to_user': self.reply_to_user,
                'reply_to_link': self.reply_to_link}

    def __str__(self):
        return \
            "\n[Tweet]\n" \
            "ID:       %s\n" \
            "User ID:  %s\n" \
            "Username: %s\n" \
            "Text:     %s\n" \
            "Time:     %s\n" \
            "R-Tweet:  %s\n" \
            "R-User:   %s\n" \
            "R-Link:   %s\n" \
            % (self.id,            self.user_id,        self.user_name,
               self.text,          self.time,           self.reply_to_tweet,
               self.reply_to_user, self.reply_to_link)
