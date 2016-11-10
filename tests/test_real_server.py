# -*- coding: utf-8 -*-
from nose.tools import assert_dict_contains_subset, assert_is_instance, assert_true
from inet.constants import SKIP_TAGS
from inet.sources import ops
from .secrets import OPS_KEY, OPS_SECRET
from unittest import skipIf


@skipIf('real' in SKIP_TAGS, 'Skipping tests that hit the real API server.')
def test_request_response():
    client = ops.OpsClient(OPS_KEY, OPS_SECRET)
    response = client.applicant_search('John')

    assert_dict_contains_subset({'Content-Type': 'application/json'}, response.headers)
    assert_true(response.ok)
    assert_is_instance(response.json(), dict)
