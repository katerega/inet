# -*- coding: utf-8 -*-
import pytest

from inet.sources.companies_house import ch_client


class TestChwrapperIntegration():
    """Test class for chwrapper Search object import"""
    def test_authd(self):
        assert ch_client._ch.session.verify is not False

if __name__ == '__main__':
    pytest.main()
