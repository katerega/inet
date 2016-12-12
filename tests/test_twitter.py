# -*- coding: utf-8 -*-
import pytest
import tweepy
import vcr

from secrets import TWITTER_ACCESS, TWITTER_SECRET
from secrets import TWITTER_CONSUMER_ACCESS, TWITTER_CONSUMER_SECRET


class TestTweepyIntegration():
    """Test class to ensure tweepy functionality works as expected"""
    # Class level client to use across tests
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_ACCESS, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS, TWITTER_SECRET)

    @vcr.use_cassette('fixtures/vcr_cassettes/twitter.yaml')
    def test_authd(self):
        api = tweepy.API(self.auth)
        assert api.verify_credentials() is not False

if __name__ == '__main__':
    pytest.main()
