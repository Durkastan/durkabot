from unittest.mock import MagicMock

from extensions.booksearch.handlers import WaqfeyaHandler


class TestWaqfeyaHandler:
    def test_init(self):
        wh = WaqfeyaHandler(MagicMock())

        assert wh.ctx is not None
        assert wh.loop is not None
