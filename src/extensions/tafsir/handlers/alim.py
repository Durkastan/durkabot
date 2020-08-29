import bs4

from extensions.tafsir.tafsir_handler import TafsirHandler, TafsirData


def clean_text(text):
    return text.replace('`', "'") \
        .replace('bin', 'b. ') \
        .replace('Hadith', 'hadith') \
        .replace('Messenger of Allah', 'Messenger of Allah ﷺ') \
        .replace('«', '#«') \
        .replace('»', '»#') \
        .replace(' "', ' #"') \
        .replace('." ', '."#') \
        .replace('﴿', '#') \
        .replace('﴾', '#')


class Alim(TafsirHandler):
    _url = "http://www.alim.org/library/quran/AlQuran-tafsir/{tafsir_id}/{surah_num}/{ayah_num}"

    _tafsirs = {
        "ibnkathir": "TIK",
        "maududi": "MDD",
        "saranbi": "ASB"
    }

    # english only
    _language = "en"

    def is_supported(self, tafsir, language) -> bool:
        return language == self._language and tafsir in self._tafsirs

    def tafsirs(self):
        return self._tafsirs.keys()

    def languages(self):
        return [self._language]

    def get_url(self, req, tafsir, language) -> str:
        tafsir_id = self._tafsirs[tafsir]

        request = req.split(':')
        surah_num = int(request[0])
        ayah_num = int(request[1])

        return self._url.format(
            tafsir_id=tafsir_id,
            surah_num=surah_num,
            ayah_num=ayah_num)

    def parse(self, response) -> TafsirData:
        soup = bs4.BeautifulSoup(response, "html.parser")

        content =  soup.find("div", {'id': "clip-all-content"})
        if content is not None:  # no tafsir found, e.g: 12:55
            tafsir_text = clean_text(content.get_text().strip())

            header = soup.find("div", {"class": "view-header"})

            ayah_tag = header.find("div", {'class': "arabic_text_style"})
            ayah_tag.find("span").decompose()
            ayah_text = ayah_tag.get_text().strip()

            header_line = header.get_text().strip()
            tafsir_name = header_line.split("- ")[0]
            surah_name = header_line.split("- ")[1].split(",")[0]

            return TafsirData(ayah_text, tafsir_text, tafsir_name, surah_name)
        else:
            return TafsirData("", "", "", "Couldn't find tafsir for this verse. Please try another tafsir.")
