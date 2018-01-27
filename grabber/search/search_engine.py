import logging
import oauth2
import json
import time

import grabber.search.tweet_util as tweet_util
import grabber.exporter.exporter as exporter
from grabber.models.tweet import Tweet
from .config.config import Config


class TweetSearchEngine:

    def get_tweets(self, criteria, backup_each=100):
        results = []
        unique_ids = set()

        active = True
        while active:
            json_response = self.get_tweets_set(criteria)

            if json_response.get('errors') is not None:
                error = json_response.get('errors')[0]
                logging.error('API error -  %s | Code - %s' % (error['message'], error['code']))
                break

            tweets = json_response['statuses']
            logging.info('Tweets in response: %d' % len(tweets))
            logging.info('Found replies:      %5d / %5d' % (len(results), criteria.count))
            if len(tweets) == 0:
                logging.warning('No more tweets')
                break

            for tweet_item in tweets:
                if tweet_util.is_reply(tweet_item):
                    tweet, unique_ids = self.__process_tweet(tweet_item, unique_ids)
                    results.append(tweet)

                if len(results) > 0 and len(results) % backup_each == 0:
                    exporter.create_tweet_dump(results)

                if criteria.count <= len(results):
                    break

            if criteria.count <= len(results):
                break

        return results

    def get_tweets_set(self, criteria):
        prefix = 'https://api.twitter.com/1.1/search/tweets.json?'
        payload = "tweet_mode=extended&count=100&lang=ru&l=[lang]&q=since:[since-date]&result_type=[result-type]"

        payload = payload.replace('[lang]', criteria.lang)
        payload = payload.replace('[since-date]', criteria.since)
        payload = payload.replace('[result-type]', criteria.result_type)

        payload = payload.replace(' ', '%20').replace(':', '%3A')

        url = prefix + payload
        logging.info('Sending request to: %s' % url)

        resp = self.__oauth_request(url).decode()
        return json.loads(resp)

    def get_dialogs(self, tweets, backup_each=100):
        prefix = 'https://api.twitter.com/1.1/statuses/show.json?tweet_mode=extended&id='
        dialogs = []
        for i, tweet in enumerate(tweets):
            dialog = [tweet]
            temp_tweet = tweet
            logging.info('Dialog: %5d / %5d' % (i, len(tweets)))
            while True:
                temp_tweet, _ = self.__get_reply(prefix + temp_tweet.reply_to_tweet)
                if temp_tweet is None:
                    break

                dialog.append(temp_tweet)

                if temp_tweet.reply_to_tweet is None:
                    break

            if len(dialog) > 1:
                dialogs.append(dialog[::-1])

            if len(dialogs) > 0 and len(dialogs) % backup_each == 0:
                exporter.create_dialog_dump(dialogs)

        return dialogs

    @staticmethod
    def __oauth_request(url, delay=5):
        time.sleep(delay)
        consumer = oauth2.Consumer(key=Config.CONSUMER_KEY, secret=Config.CONSUMER_SECRET)
        token = oauth2.Token(key=Config.TOKEN, secret=Config.TOKEN_SECRET)
        client = oauth2.Client(consumer, token)
        resp, content = client.request(url)
        return content

    @staticmethod
    def __process_tweet(tweet_item, unique_ids=None):

        tweet_id = tweet_item.get('id_str', None)
        if tweet_id is None:
            return None, None

        if unique_ids is not None:
            if tweet_id not in unique_ids:
                unique_ids.add(tweet_id)
            else:
                return None, None

        tweet = Tweet()
        tweet.id = tweet_item['id_str']
        tweet.user_id = tweet_item['user']['id_str']
        tweet.user_name = tweet_item['user']['screen_name']
        tweet.text = tweet_item['full_text']
        tweet.time = tweet_item['created_at']

        if tweet_item['in_reply_to_status_id_str'] is not None:
            tweet.reply_to_tweet = tweet_item['in_reply_to_status_id_str']
            tweet.reply_to_user = tweet_item['in_reply_to_screen_name']
            tweet.reply_to_link = \
                'https://twitter.com/' + tweet.reply_to_user + \
                "/status/" + tweet_item['in_reply_to_status_id_str']

        return tweet, unique_ids

    def __get_reply(self, url):
        json_tweet = self.__oauth_request(url, 1)
        return self.__process_tweet(json.loads(json_tweet.decode()))
