class HadithRequest:
    url1 = 'https://sunnah.com/{}/{}'  # for qudsi/nawawi
    url2 = 'https://sunnah.com/{}/{}/{}'  # for all others

    def __init__(self, book_name, ref):
        self.book_name = book_name
        self.book_number = None
        self.hadith_number = None

        if self.book_name == 'qudsi' or book_name == 'nawawi':
            self.formatted_book_name = self.book_name + '40'
            self.hadith_number = ref
        else:
            self.book_number, self.hadith_number = ref.split(":")

    @property
    def url(self):
        if self.book_name == 'qudsi' or self.book_name == 'nawawi':
            return self.url1.format(self.formatted_book_name, self.hadith_number)
        else:
            return self.url2.format(self.book_name, self.book_number, self.hadith_number)
