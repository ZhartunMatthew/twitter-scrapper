
class SearchCriteria:

    def __init__(self):
        self.lang = None
        self.count = None
        self.since = None
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

    def set_max_position(self, max_position):
        self.max_position = max_position
        return self

    def __str__(self):
        return \
            '\n[SearchCriteria]\n' \
            'Lang:         %s\n' \
            'Count:        %s\n' \
            'Since:        %s\n' \
            'Result type:  %s\n' \
            'Max position: %s\n' \
            % (self.lang, self.count, self.since, self.result_type, self.max_position)
