from unittest.mock import MagicMock

import pytest
from discord.ext.commands import Context

from main import Bot


@pytest.fixture
def ctx():
    Context(prefix='durka', bot=MagicMock(spec=Bot), message=MagicMock())
