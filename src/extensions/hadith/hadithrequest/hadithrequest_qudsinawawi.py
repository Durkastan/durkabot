class HadithRequestQudsiNawawi:
    _url = 'https://sunnah.com/{}/{}'

    def __init__(self, book_name, ref):
        self.book_name = book_name + '40'
        self.hadith_number = ref

    @property
    def url(self):
        return self._url.format(self.book_name, self.hadith_number)
