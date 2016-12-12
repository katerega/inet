# -*- coding: utf-8 -*-
import pytest
import vcr

from inet.sources.twitter import api


class TestTweepyIntegration():
    """Test class to ensure tweepy functionality works as expected"""
    @vcr.use_cassette('fixtures/vcr_cassettes/twitter.yaml')
    def test_authd(self):
        assert api.verify_credentials() is not False

if __name__ == '__main__':
    pytest.main()
