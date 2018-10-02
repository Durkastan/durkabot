from extensions.quran.quranrequest import QuranRequest


def test_init_parses_parameters():
    test_table = { # req, edition: surah, offset, limit, edition
        ("5:20", 'asad'): (5, 19, 1,  'en.asad'),
        ("20:20-29", 'ar'): (20, 19, 10,  'ar'),
        ("114:1-5", 'sahih'): (114, 0, 5,  'en.sahih')
    }
    for (req, raw_edition), (surah, offset, limit, edition) in test_table.items():
        q = QuranRequest(req, raw_edition)
        assert q.surah == surah
        assert q.offset == offset
        assert q.limit == limit
        assert q.edition == edition
