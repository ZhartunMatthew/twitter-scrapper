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
        self.query = None
        self.count = None
        self.since = None
        self.until = None
        self.result_type = None

    def set_query(self, query):
        self.query = query
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
