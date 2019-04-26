from extensions.hadith.hadithrequest.hadithrequest_general import HadithRequestGeneral
from extensions.hadith.hadithrequest.hadithrequest_qudsinawawi import HadithRequestQudsiNawawi


def get_hadith_request(book_name, ref):
    if book_name == 'qudsi' or book_name == 'nawawi':
        return HadithRequestQudsiNawawi(book_name, ref)
    else:
        return HadithRequestGeneral(book_name, ref)
