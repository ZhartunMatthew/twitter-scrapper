import logging
import oauth2
import json
import time

import grabber.search.tweet_util as tweet_util
from grabber.models.tweet import Tweet
from .config.config import Config


class TweetSearchEngine:

    @staticmethod
    def get_tweets(criteria):
        results = []
        unique_ids = set()

        active = True
        while active:
            time.sleep(20)
            json_response = TweetSearchEngine.get_tweets_set(criteria)

            if json_response.get('errors') is not None:
                error = json_response.get('errors')[0]
                logging.error('API error -  %s | Code - %s' % (error['message'], error['code']))
                break

            tweets = json_response['statuses']
            logging.info('Found tweets: %d' % len(tweets))
            if len(tweets) == 0:
                logging.warning('No more tweets')
                break

            for tweet_item in tweets:
                if tweet_util.is_reply(tweet_item):
                    tweet = Tweet()
                    tweet.id = tweet_item['id_str']
                    tweet.author = tweet_item['user']['id_str']
                    tweet.text = tweet_item['text']
                    tweet.reply_to = tweet_item['in_reply_to_status_id_str']
                    tweet.time = tweet_item['created_at']
                    logging.info('Found: %d' % len(results))
                    if tweet.id not in unique_ids:
                        unique_ids.add(tweet.id)
                        results.append(tweet)

                if criteria.count <= len(results):
                    break

            if criteria.count <= len(results):
                break

        return results

    @staticmethod
    def get_tweets_set(criteria):
        logging.info(criteria)
        # prefix = 'https://twitter.com/i/search/timeline?'
        # payload = "lang=ru&l=[lang]&q=since:[since-date] until:[until-date]&max_position=[max-position]"
        prefix = 'https://api.twitter.com/1.1/search/tweets.json?'
        payload = "lang=ru&l=[lang]&q=since:[since-date]&result_type=[result-type]"

        payload = payload.replace('[lang]', criteria.lang)
        payload = payload.replace('[since-date]', criteria.since)
        payload = payload.replace('[result-type]', criteria.result_type)

        payload = payload.replace(' ', '%20').replace(':', '%3A')

        url = prefix + payload
        logging.info('Sending request to: %s' % url)

        resp = TweetSearchEngine.__oauth_request(url).decode()
        return json.loads(resp)

    @staticmethod
    def __oauth_request(url):
        consumer = oauth2.Consumer(key=Config.CONSUMER_KEY, secret=Config.CONSUMER_SECRET)
        token = oauth2.Token(key=Config.TOKEN, secret=Config.TOKEN_SECRET)
        client = oauth2.Client(consumer, token)
        resp, content = client.request(url)
        return content
