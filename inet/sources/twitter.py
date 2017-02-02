# -*- coding: utf-8 -*-
import itertools

import tweepy

from .constants import TWITTER_ACCESS, TWITTER_SECRET
from .constants import TWITTER_CONSUMER_ACCESS, TWITTER_CONSUMER_SECRET

_auth = tweepy.OAuthHandler(TWITTER_CONSUMER_ACCESS, TWITTER_CONSUMER_SECRET)
_auth.set_access_token(TWITTER_ACCESS, TWITTER_SECRET)

twitter_client = tweepy.API(_auth, wait_on_rate_limit=True)


class TwitterHandler():
    """Handles custom queries through Tweepy"""
    def __init__(self):
        self.twitter_client = twitter_client

    def paginate(self, iterable, page_size):
        while True:
            i1, i2 = itertools.tee(iterable)
            iterable, page = (itertools.islice(i1, page_size, None),
                              list(itertools.islice(i2, page_size)))
            if len(page) == 0:
                break
            yield page

    def followers(self, handles):
        """Return a dictionary of followers by handle."""
        print(handles)
        followers_list = {}
        for handle in handles:
            followers = self.twitter_client.followers_ids(screen_name=handle)

            r = []
            for page in self.paginate(followers, 100):
                results = self.twitter_client.lookup_users(user_ids=page)
                for result in results:
                    r.append(result.screen_name)
            followers_list[handle] = r
        return followers_list

    def following(self, handles):
        following_list = {}
        for handle in handles:
            following = self.twitter_client.friends_ids(screen_name=handle)

            r = []
            for page in self.paginate(following, 100):
                results = self.twitter_client.lookup_users(user_ids=page)
                for result in results:
                    r.append(result.screen_name)
            following_list[handle] = r
        return following_list


twitter_handler = TwitterHandler()
