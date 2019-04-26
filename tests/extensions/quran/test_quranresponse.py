import json

from extensions.quran.quranresponse import QuranResponse


def test_init_parses_surah_data_in_response():
    sample = json.load(open("res/extensions/quran/response_samples.json", 'r'))
    test_table = [  # surah_num, arabic_name, english_name, revelation_type, num_ayahs, language, edition
        (sample[0], (5, "سورة المائدة", "Al-Maaida", "Medinan", 120, 'en', "Muhammad Asad")),
        (sample[1], (20, "سورة طه", "Taa-Haa", "Meccan", 135, 'ar', "Simple")),
        (sample[2], (114, "سورة الناس", "An-Naas", "Meccan", 6, 'en', "Saheeh International")),
    ]
    for sample, (surah_num, arabic_name, english_name,
                 revelation_type, num_ayahs, language, edition) in test_table:
        q = QuranResponse(sample)
        assert q.surah_number == surah_num
        assert q.surah_arabic_name == arabic_name
        assert q.surah_english_name == english_name
        assert q.surah_revelation_type == revelation_type
        assert q.surah_num_ayahs == num_ayahs
        assert q.language == language
        assert q.edition_name == edition


def test_init_parses_ayah_data_in_response():
    sample = json.load(open("res/extensions/quran/response_samples.json", 'r'))
    test_table = [  # num of ayat, (length_1, length_2, ...)
        (sample[0], (1, (257, ))),
        (sample[1], (10, (42, 63, 85, 36, 40, 31, 21, 32, 18, 35))),
        (sample[2], (5, (43, 25, 19, 43, 49))),
    ]
    for sample, (num_of_ayat, lengths) in test_table:
        q = QuranResponse(sample)
        assert len(q.ayahs) == num_of_ayat
        for text in q.ayahs.values():
            assert len(text) in lengths
