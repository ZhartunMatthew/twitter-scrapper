class Tweet:
    def __init__(self):
        self.id = None
        self.author = None
        self.text = None
        self.reply_to = None
        self.time = None

    def to_dict(self):
        return {'id': self.id,
                'author': self.author,
                'time': self.time,
                'reply_to': self.reply_to,
                'text': self.text}

    def __str__(self):
        return \
            "\n[Tweet]\n" \
            "ID:       %s\n" \
            "Author:   %s\n" \
            "Text:     %s\n" \
            "Reply to: %s\n" \
            "Time:     %s" \
            % (self.id, self.author, self.text, self.reply_to, self.time)
