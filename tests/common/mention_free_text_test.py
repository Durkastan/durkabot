from unittest.mock import MagicMock

import pytest

from common.mention_free_text import MentionFreeText, NotMentionFreeException


@pytest.mark.asyncio
async def test_convert_returns_text_if_clean(ctx):
    text = "just because you have a meme command doesn't mean you're dank"
    msg = MagicMock(content=text, mentions=[], role_mentions=[])

    assert (await MentionFreeText.convert(MagicMock(spec=ctx, message=msg), text)) == text


@pytest.mark.asyncio
async def test_convert_raises_error_if_not_clean(ctx):
    test_table = [  # text, mentions, role_mentions
        ("@here", [], []),
        ("stuff", [''], []),
        ("stuff", [], ['']),
        ("@everyone", [''], [])
    ]
    for text, mentions, role_mentions in test_table:
        msg = MagicMock(content=text, mentions=mentions, role_mentions=role_mentions)

        with pytest.raises(NotMentionFreeException):
            await MentionFreeText.convert(MagicMock(spec=ctx, message=msg), text)
