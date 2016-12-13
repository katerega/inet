# -*- coding: utf-8 -*-
import tweepy

from .constants import TWITTER_ACCESS, TWITTER_SECRET
from .constants import TWITTER_CONSUMER_ACCESS, TWITTER_CONSUMER_SECRET

_auth = tweepy.OAuthHandler(TWITTER_CONSUMER_ACCESS, TWITTER_CONSUMER_SECRET)
_auth.set_access_token(TWITTER_ACCESS, TWITTER_SECRET)

twitter_client = tweepy.API(_auth)
