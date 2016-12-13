# -*- coding: utf-8 -*-
import pytest

from inet.sources.companies_house import ch_api


class TestTweepyIntegration():
    """Test class for chwrapper Search object import"""
    def test_authd(self):
        assert ch_api.session.verify is not False

if __name__ == '__main__':
    pytest.main()
