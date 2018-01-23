
def is_reply(tweet):
    return tweet['in_reply_to_status_id'] is not None
