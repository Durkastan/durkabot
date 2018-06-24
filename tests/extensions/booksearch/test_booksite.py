from unittest.mock import MagicMock

import pytest

from extensions.booksearch.booksite import BookSite, UnSupportedSite
from extensions.booksearch.handlers import WaqfeyaHandler


def test_init(ctx):
    b = BookSite(MagicMock(spec=ctx), MagicMock(spec=WaqfeyaHandler))

    assert b is not None
    assert b.handler is not None
    assert b.ctx is not None


@pytest.mark.asyncio
async def test_convert_returns_object_if_supported_site(ctx):
    site = 'waqfeya'
    assert site in BookSite.supported_sites

    assert isinstance(await BookSite.convert(MagicMock(spec=ctx), site), BookSite)


@pytest.mark.asyncio
async def test_convert_raises_error_if_not_supported_site(ctx):
    site = 'nonexistentlibrary'
    assert site not in BookSite.supported_sites

    with pytest.raises(UnSupportedSite):
        await BookSite.convert(MagicMock(spec=ctx), site)
