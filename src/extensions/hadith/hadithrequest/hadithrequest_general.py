class HadithRequestGeneral:
    _url = 'https://sunnah.com/{}/{}/{}'

    def __init__(self, book_name, ref):
        self.book_name = book_name
        self.book_number, self.hadith_number = ref.split(":")

    @property
    def url(self):
        return self._url.format(self.book_name, self.book_number, self.hadith_number)
