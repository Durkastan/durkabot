from unittest.mock import Mock, MagicMock

import pytest
from pymongo import MongoClient

from storage import StorageHandler


GUILD_ID = 12345


@pytest.fixture
def storage():
    ctx_mock = Mock(guild=Mock(id=GUILD_ID))
    s = StorageHandler(ctx_mock)
    s._get_db = MagicMock()
    s._get_client = MagicMock()
    return s


def test_init(storage):
    assert storage.database_name == 'db_' + str(GUILD_ID)


def test_client_lazily_creates_client(storage):
    storage._get_client.return_value = client = MagicMock(spec=MongoClient)

    assert storage._client is None
    assert storage.client == client
    assert storage._client == client


def test_db_lazily_creates_db(storage):
    storage._get_db.return_value = db = MagicMock(spec=MongoClient)

    assert storage._db is None
    assert storage.db == db
    assert storage._db == db
