from extensions.hadith.hadithrequest import HadithRequestGeneral


class TestHadithRequestGeneral:
    def test_init_parses_parameters(self):
        test_table = {  # input_book_name, ref: book_name, book_number, hadith_number
            ("bukhari", '1:1'): ("bukhari", '1', '1'),
            ("tirmidhi", '2:5'): ("tirmidhi", "2", "5"),
            ("muslim", "5:2"): ("muslim", "5", "2")
        }
        for (input_book_name, ref), (book_name, book_number, hadith_number) in test_table.items():
            h = HadithRequestGeneral(input_book_name, ref)

            assert h.book_name == book_name
            assert h.book_number == book_number
            assert h.hadith_number == hadith_number

    def test_url_formats_url_from_data(self):
        test_table = {
            ("bukhari", '1', '1'): "https://sunnah.com/bukhari/1/1",
            ("tirmidhi", "2", "5"): "https://sunnah.com/tirmidhi/2/5",
            ("muslim", "5", "2"): "https://sunnah.com/muslim/5/2"
        }
        for (book_name, book_number, hadith_number), url in test_table.items():
            h = HadithRequestGeneral("", "1:2")

            h.book_name = book_name
            h.book_number = book_number
            h.hadith_number = hadith_number

            assert h.url == url
