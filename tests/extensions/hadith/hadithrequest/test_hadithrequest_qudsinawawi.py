from extensions.hadith.hadithrequest import HadithRequestQudsiNawawi


class TestHadithRequestQudsiNawawi:
    def test_init_parses_parameters(self):
        test_table = {  # input_book_name, ref: book_name, hadith_number
            ("nawawi", '4'): ("nawawi40", '4'),
            ("qudsi", "5"): ("qudsi40", '5')
        }
        for (input_book_name, ref), (book_name, hadith_number) in test_table.items():
            h = HadithRequestQudsiNawawi(input_book_name, ref)

            assert h.book_name == book_name
            assert h.hadith_number == hadith_number

    def test_url_formats_url_from_data(self):
        test_table = {
            ("nawawi40", '4'): "https://sunnah.com/nawawi40/4",
            ("qudsi40", '5'): "https://sunnah.com/qudsi40/5"
        }
        for (book_name, hadith_number), url in test_table.items():
            h = HadithRequestQudsiNawawi("", "1")

            h.book_name = book_name
            h.hadith_number = hadith_number

            assert h.url == url
