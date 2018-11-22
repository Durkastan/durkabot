import os
import sys

# only apply hack if we're not running a specialized test
if 'tests' not in os.getcwd():
    os.chdir('./tests/')
    sys.path.append('../src/')

from unittest.mock import MagicMock

import pytest
from discord.ext.commands import Context

from main import Bot


@pytest.fixture
def ctx():
    Context(prefix='durka', bot=MagicMock(spec=Bot), message=MagicMock())
