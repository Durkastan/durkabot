from extensions.hadith.hadithrequest import HadithRequestForty


class TestHadithRequestForty:
    def test_init_parses_parameters(self):
        test_table = {  # input_book_name, ref: book_index, hadith_number
            ("nawawi", '4'): (1, '4'),
            ("qudsi", "5"): (2, '5'),
            ("shahwaliullah", "8"): (3, "8")
        }
        for (input_book_name, ref), (book_index, hadith_number) in test_table.items():
            h = HadithRequestForty(input_book_name, ref)

            assert h.book_index == book_index
            assert h.hadith_number == hadith_number

    def test_url_formats_url_from_data(self):
        test_table = {
            ("nawawi", '4'): "https://sunnah.com/forty/1/4",
            ("qudsi", '5'): "https://sunnah.com/forty/2/5",
            ("shahwaliullah", "8"): "https://sunnah.com/forty/3/8"
        }
        for (book_name, hadith_number), url in test_table.items():
            h = HadithRequestForty(book_name, hadith_number)

            assert h.url == url
