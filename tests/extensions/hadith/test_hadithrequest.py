from extensions.hadith.hadithrequest.hadithrequest_general import HadithRequestGeneral
from extensions.hadith.hadithrequest import get_hadith_request, HadithRequestForty


def test_get_hadith_request_returns_correct_type():
    assert isinstance(get_hadith_request('nawawi', '4'), HadithRequestForty)
    assert isinstance(get_hadith_request('qudsi', '5'), HadithRequestForty)

    assert isinstance(get_hadith_request('bukhari', '1:1'), HadithRequestGeneral)
    assert isinstance(get_hadith_request('muslim', '2:1'), HadithRequestGeneral)
    assert isinstance(get_hadith_request('tirmidhi', '5:3'), HadithRequestGeneral)
