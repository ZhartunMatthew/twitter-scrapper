class Tweet:
    def __init__(self):
        self.id = None
        self.author = None
        self.text = None
        self.reply_to = None
        self.time = None

    def __str__(self):
        return \
            "\n[Tweet]\n" \
            "ID:       %s\n" \
            "Author:   %s\n" \
            "Text:     %s\n" \
            "Reply to: %s\n" \
            "Time:     %s" \
            % (self.id, self.author, self.text, self.reply_to, self.time)
