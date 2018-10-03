from collections import OrderedDict


class QuranResponse:
    def __init__(self, response_json):
        data = response_json['data']

        self.surah_number = data['number']
        self.surah_arabic_name = data["name"]
        self.surah_english_name = data["englishName"]
        self.surah_revelation_type = data['revelationType']
        self.surah_num_ayahs = data['numberOfAyahs']

        self.ayahs = OrderedDict()

        for ayah in data['ayahs']:
            self.ayahs[ayah['numberInSurah']] = ayah['text']

        self.language = data['edition']['language']
        self.edition_name = data['edition']['englishName']
