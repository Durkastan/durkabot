import json

from extensions.quran.quraneditions import parse_editions


def test_parse_editions_reports_bad_request():
    r = {'code': 400}
    assert "Bad request" in parse_editions(r)


def test_parse_editions_returns_editions():
    sample = json.load(open("res/edition_response_sample.json", 'r'))
    expected = """```
en.ahmedali
en.ahmedraza
en.arberry
en.asad
en.daryabadi
en.hilali
en.pickthall
en.qaribullah
en.sahih
en.sarwar
en.yusufali
en.maududi
en.shakir
en.transliteration```"""

    result = parse_editions(sample)

    assert result == expected
