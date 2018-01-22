class SearchCriteria:
    """
    Used for specify search parameters
    username - searching users, annotated with @
    since - date of oldest tweet in search
    since - date of the most recent tweet in search
    querySearch - query for searching
    maxTweet - max count of tweet on response
    """
    def __init__(self):
        self.lang = None
        self.count = None
        self.since = None
        self.until = None
        self.result_type = None
        self.max_position = None

    def set_lang(self, lang):
        self.lang = lang
        return self

    def set_count(self, count):
        self.count = count
        return self

    def set_result_type(self, result_type):
        self.result_type = result_type
        return self

    def set_since(self, since):
        self.since = since
        return self

    def set_until(self, until):
        self.until = until
        return self

    def set_max_position(self, max_position):
        self.max_position = max_position
        return self

    def __str__(self):
        return '[SearchCriteria]\n' \
               'Lang:         %s\n' \
               'Count:        %s\n' \
               'Since:        %s\n' \
               'Until:        %s\n' \
               'Result type:  %s\n' \
               'Max position: %s\n' \
               % (self.lang, self.count, self.since, self.until, self.result_type, self.max_position)
