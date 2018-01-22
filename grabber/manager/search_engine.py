import http.cookiejar as cookielib
import urllib.request as ur
import logging
import json
import sys
import re

from .tweet_util import TweetUtil
from .models.tweet import Tweet
from pyquery import PyQuery


class TweetSearchEngine:

    def __init__(self):
        """
        Using for send requests to twitter search and parse response with tweets
        """
        pass

    @staticmethod
    def getTweets(criteria, show_id, proxy=None):
        """
        Using for parse json response
        :param criteria: Search criteria
        :param show_id: Show id from IMDB
        :param proxy:
        :return: Searched tweets array
        """
        refreshCursor = ''

        results = []
        cookieJar = cookielib.CookieJar()

        active = True

        while active:
            json = TweetSearchEngine.getJsonReponse(criteria, refreshCursor, cookieJar, proxy)
            if len(json['items_html'].strip()) == 0:
                break

            refreshCursor = json['min_position']
            tweets = PyQuery(json['items_html'])('div.js-stream-tweet')

            if len(tweets) == 0:
                break

            for tweetHTML in tweets:
                tweet = Tweet()

                tweet_pq = PyQuery(tweetHTML)

                user_id = tweet_pq.attr("data-user-id")
                tweet_timestamp = int(tweet_pq("small.time span.js-short-timestamp").attr("data-time"))
                txt = re.sub(r"\s+", " ", tweet_pq("p.js-tweet-text")
                             .text().replace('# ', '#').replace('@ ', '@')).replace(' imdb', 'imdb')

                if user_id is None or txt is None or tweet_timestamp is None:
                    continue

                tweet.user_id = user_id
                tweet.show_id = show_id
                tweet.timestamp = tweet_timestamp
                tweet.show_rating = TweetUtil.extract_rating(txt)

                if not str(tweet.user_id).isdigit():
                    continue

                if tweet.show_id == -1:
                    continue

                if tweet.show_rating.isdigit():
                    if int(tweet.show_rating) > 10 or int(tweet.show_rating) < 0:
                        continue
                else:
                    continue

                results.append(tweet)

                if criteria.maxTweets <= len(results):
                    break

            if criteria.maxTweets <= len(results):
                break

        return results

    @staticmethod
    def getJsonReponse(criteria, refreshCursor, cookieJar, proxy):
        """
        Using for send request to twitter search
        :param criteria: Search criteria
        :param refreshCursor: Refresh cursor for getting new tweets
        :param cookieJar: Session cookie
        :param proxy:
        :return: json response with tweets
        """
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

        urlGetData = ''

        if hasattr(criteria, 'username'):
            urlGetData += ' from:' + criteria.username

        if hasattr(criteria, 'querySearch'):
            urlGetData += ' ' + criteria.querySearch

        if hasattr(criteria, 'since'):
            urlGetData += ' since:' + criteria.since

        if hasattr(criteria, 'until'):
            urlGetData += ' until:' + criteria.until

        url = url % (ur.quote(urlGetData), refreshCursor)

        headers = [
            ('Host', "twitter.com"),
            ('User-Agent', "Chrome/60.0.3112.90"),
            ('Accept', "application/json, text/javascript, */*; q=0.01"),
            ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
            ('X-Requested-With', "XMLHttpRequest"),
            ('Referer', url),
            ('Connection', "keep-alive")
        ]

        if proxy:
            opener = ur.build_opener(ur.ProxyHandler({'http': proxy, 'https': proxy}),
                                     ur.HTTPCookieProcessor(cookieJar))
        else:
            opener = ur.build_opener(ur.HTTPCookieProcessor(cookieJar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            jsonResponse = response.read()
        except:
            logging.info("Twitter weird response. "
                         "Try to see on browser: https://twitter.com/search?q=%s&src=typd" % ur.quote(urlGetData))
            sys.exit()

        dataJson = json.loads(jsonResponse)

        return dataJson