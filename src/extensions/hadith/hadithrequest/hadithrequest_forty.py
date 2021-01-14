class HadithRequestForty:
    _url = 'https://sunnah.com/forty/{}/{}'
    _collection_indexes = {
        'nawawi': 1,
        'qudsi': 2,
        'shahwaliullah': 3
    }

    def __init__(self, book_name, ref):
        self.book_index = self._collection_indexes[book_name]
        self.hadith_number = ref

    @property
    def url(self):
        return self._url.format(self.book_index, self.hadith_number)
