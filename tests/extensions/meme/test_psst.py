from extensions.meme.psst import split_txt


def test_split_txt_splits_text():
    num_segments = 5
    txt = "just because you have a meme command doesn't mean you're dank"

    result = split_txt(txt, num_segments)
    assert result == ['just because', 'you have', 'a meme', "command doesn't", "mean you're dank"]
