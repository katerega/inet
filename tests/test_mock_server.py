# -*- coding: utf-8 -*-
import pytest
import requests

from http.server import BaseHTTPRequestHandler
from inet.sources import ops
from nose.tools import assert_dict_contains_subset, assert_true
from .secrets import OPS_KEY, OPS_SECRET
from tests.mocks import get_free_port, start_mock_server
from unittest.mock import patch


class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Process an HTTP GET request and return a response with an HTTP 200 status.
        self.send_response(requests.codes.ok)
        self.end_headers()
        return


class TestMockServer(object):
    @classmethod
    def setup_class(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_request_response(self):
        mock_users_url = 'http://localhost:{port}/'.format(port=self.mock_server_port)
        client = ops.OpsClient(OPS_KEY, OPS_SECRET)

        # Patch USERS_URL so that the service uses the mock server URL instead of the real URL.
        with patch.dict('inet.services.__dict__', {'USERS_URL': mock_users_url}):
            response = client.applicant_search('John')

        assert_dict_contains_subset({'Content-Type': 'application/json'}, response.headers)
        assert_true(response.ok)


if __name__ == "__main__":
    pytest.main()
