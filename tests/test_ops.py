# -*- coding: utf-8 -*-
import pytest

from epo_ops.middlewares import Dogpile, Throttler
from epo_ops.middlewares.throttle.storages import sqlite
from inet.sources.ops import OpsClient
from secrets import OPS_KEY, OPS_SECRET


def test_ops_client_instantiated():
    """Test our subclass od epo_ops.RegisteredClient
    to ensure it is instantiatied correctly."""
    client = OpsClient(OPS_KEY, OPS_SECRET)
    assert len(client.middlewares) == 1
    assert client.middlewares[0].history.db_path == sqlite.DEFAULT_DB_PATH

    middlewares = [
        Dogpile(),
        Throttler(),
    ]

    client = OpsClient(OPS_KEY,
                       OPS_SECRET,
                       accept_type='JSON',
                       middlewares=middlewares)
    assert len(client.middlewares) == 2


if __name__ == '__main__':
    pytest.main()
