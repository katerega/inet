# -*- coding: utf-8 -*-
import pytest
import vcr

from inet.sources import ops
from inet.sources.ops import OpsClient
from epo_ops.middlewares import Dogpile, Throttler
from epo_ops.middlewares.throttle.storages import sqlite
from nose.tools import assert_dict_contains_subset, assert_is_instance, assert_true
from .secrets import OPS_KEY, OPS_SECRET


class TestOps():
    # Class level client to use across tests
    client = ops.OpsClient(OPS_KEY, OPS_SECRET)

    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_request_response(self):
        response = self.client.applicant_search('John')
        assert_dict_contains_subset({'Content-Type': 'application/json'}, response.headers)
        assert_true(response.ok)
        assert_is_instance(response.json(), dict)

    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_ops_client_instantiated(self):
        """Test our subclass od epo_ops.RegisteredClient
        to ensure it is instantiatied correctly."""
        assert len(self.client.middlewares) == 1
        assert self.client.middlewares[0].history.db_path == sqlite.DEFAULT_DB_PATH

        middlewares = [
            Dogpile(),
            Throttler(),
        ]

        client = OpsClient(OPS_KEY,
                           OPS_SECRET,
                           accept_type='JSON',
                           middlewares=middlewares)
        assert len(client.middlewares) == 2

    @vcr.use_cassette('fixtures/vcr_cassettes/synopsis.yaml')
    def test_ops_searches(self):
        result = self.client.inventor_search("John")
        assert result.ok is True

    def test_ops_client_no_key(self):
        with pytest.raises(TypeError):
            OpsClient()

if __name__ == '__main__':
    pytest.main()
