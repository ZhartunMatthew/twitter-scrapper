class Tweet:
    def __init__(self):
        self.id = None
        self.user_id = None
        self.user_name = None
        self.text = None
        self.time = None
        self.link = None
        self.is_truncated = None
        self.reply_to_tweet = None
        self.reply_to_user = None
        self.reply_to_link = None

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'user_name': self.user_name,
                'text': self.text,
                'time': self.time,
                'link': self.link,
                'is_truncated': self.is_truncated,
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
            "Link:     %s\n" \
            "Trunc:    %s\n" \
            "R-Tweet:  %s\n" \
            "R-User:   %s\n" \
            "R-Link:   %s\n" \
            % (self.id,           self.user_id,        self.user_name,
               self.text,         self.time,           self.link,
               self.is_truncated, self.reply_to_tweet, self.reply_to_user, self.reply_to_link)
