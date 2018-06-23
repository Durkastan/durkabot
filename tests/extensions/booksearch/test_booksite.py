from unittest.mock import MagicMock

import pytest
from discord.ext.commands import Context

from extensions.booksearch.booksite import BookSite, UnSupportedSite
from extensions.booksearch.handlers import WaqfeyaHandler


def test_init():
    b = BookSite(MagicMock(spec=Context), MagicMock(spec=WaqfeyaHandler))

    assert b is not None
    assert b.handler is not None
    assert b.ctx is not None


@pytest.mark.asyncio
async def test_convert_returns_object_if_supported_site():
    site = 'waqfeya'
    assert site in BookSite.supported_sites

    assert isinstance(await BookSite.convert(MagicMock(), site), BookSite)


@pytest.mark.asyncio
async def test_convert_raises_error_if_not_supported_site():
    site = 'nonexistentlibrary'
    assert site not in BookSite.supported_sites

    with pytest.raises(UnSupportedSite):
        await BookSite.convert(MagicMock(spec=Context), site)
