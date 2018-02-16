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
                    if tweet is not None:
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

    def get_dialogs(self, tweets, batch_size):
        res_dialogs = []
        offset = 100
        tweets_count = len(tweets)

        for i in range(0, int(tweets_count / offset)):
            logging.info('Fetching dialogs:      %5d / %5d' % (i, int(tweets_count / offset)))
            tweets_slice = tweets[i * offset:i * offset + offset]
            dialogs = [[t] for t in tweets_slice]
            min_amount = 3
            stop_amount = 5

            while stop_amount > 0:
                tweets_slice = self.__get_dialogs_batch(tweets_slice)
                dialogs = self.__match_tweets(dialogs, tweets_slice)

                if len(tweets_slice) <= min_amount:
                    stop_amount -= 1

            res_dialogs += dialogs

            if len(res_dialogs) >= batch_size:
                for d in res_dialogs:
                    d.reverse()
                exporter.create_dialog_dump(res_dialogs)
                res_dialogs = []

    @staticmethod
    def __match_tweets(dialogs, replies):
        for reply in replies:
            for dialog in dialogs:
                if reply.id == dialog[-1].reply_to_tweet:
                    dialog.append(reply)
                    break

        return dialogs

    def __get_dialogs_batch(self, tweets_slice):
        prefix = 'https://api.twitter.com/1.1/statuses/lookup.json?tweet_mode=extended&id='
        for tweet in tweets_slice:
            if tweet.reply_to_tweet is not None:
                prefix += tweet.reply_to_tweet + ','

        json_resp = self.__oauth_request(prefix[:-1], 3).decode()
        resp = json.loads(json_resp)
        tweets = []
        for json_tweet in resp:
            try:
                processed_tweet, _ = self.__process_tweet(json_tweet)
                tweets.append(processed_tweet)
            except AttributeError:
                logging.info(str(json_resp))
                time.sleep(2)

        return tweets

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

