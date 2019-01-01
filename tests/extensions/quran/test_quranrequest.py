from extensions.quran.quranrequest import QuranRequest


def test_init_parses_parameters():
    test_table = {  # req, edition: surah, offset, limit, edition
        ("5:20", 'asad'): (5, 19, 1,  'en.asad'),
        ("20:20-29", 'ar.simple'): (20, 19, 10,  'ar.simple'),
        ("114:1-5", 'sahih'): (114, 0, 5,  'en.sahih'),
        ("18:9-10", "en.pickthall"): (18, 8, 2, 'en.pickthall'),
        ("3:7", 'ar'): (3, 6, 1, 'en.ar')  # invalid edition, api returns arabic. good enough
    }
    for (req, raw_edition), (surah, offset, limit, edition) in test_table.items():
        q = QuranRequest(req, raw_edition)
        assert q.surah == surah
        assert q.offset == offset
        assert q.limit == limit
        assert q.edition == edition


def test_url_formats_url_from_data():
    test_table = {
        (5, 19, 1,  'en.asad'): "http://api.alquran.cloud/surah/5/en.asad?offset=19&limit=1",
        (20, 19, 10,  'ar'): "http://api.alquran.cloud/surah/20/ar?offset=19&limit=10",
        (114, 0, 5,  'en.sahih'): "http://api.alquran.cloud/surah/114/en.sahih?offset=0&limit=5"
    }
    for (surah, offset, limit, edition), url in test_table.items():
        q = QuranRequest('1:1', 'ar')
        q.surah = surah
        q.offset = offset
        q.limit = limit
        q.edition = edition

        assert q.url == url
