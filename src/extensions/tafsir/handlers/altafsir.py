import bs4
from bs4 import Tag, NavigableString

from extensions.tafsir.tafsir_handler import TafsirData, TafsirHandler


def remove_child(parent, child_index):
    child = parent.contents[child_index]
    if isinstance(child, Tag):
        child.decompose()
    elif isinstance(child, NavigableString):
        parent.contents.remove(child)


def extract_text(soup):
    text: Tag = soup.find("div", {'id': "SearchResults"})

    remove_child(text, 0)

    subtxt = text.contents[-1]
    remove_child(subtxt, -1)

    separator = subtxt.find("hr")
    if separator:
        separator_index = subtxt.contents.index(separator)
        while len(subtxt.contents) - 1 > separator_index:
            remove_child(subtxt, separator_index)

    s = text.get_text()
    ind = s.find("}")
    return s[:ind + 1], s[ind + 1:]


class AlTafsir(TafsirHandler):
    _url = ("https://www.altafsir.com/Tafasir.asp?"
            "tMadhNo=0&"
            "tDisplay=yes&"
            "LanguageId={language_id}&"
            "tTafsirNo={tafsir_id}&"
            "tSoraNo={surah_num}&"
            "tAyahNo={ayah_num}")

    _languages = {
        "en": 2,
        "ar": 1
    }

    _tafsirs = {
        "tabari": {"ar": 1},
        "zamakhshari": {"ar": 2},
        "tabrasi": {"ar": 3},
        "razi": {"ar": 4},
        "qurtubi": {"ar": 5},
        "baydawi": {"ar": 6},
        "ibnkathir": {"ar": 7},
        "jalalayn": {"ar": 8, "en": 74},
        "shawkani": {"ar": 9},
        "fairuzabadi": {"ar": 10},
        "samarqandi": {"ar": 11},
        "mawardi": {"ar": 12},
        "baghawi": {"ar": 13},
        "ibnattiyah": {"ar": 14},
        "ibnaljawzi": {"ar": 15},
        "ibnabdalsalam": {"ar": 16},
        "nasafi": {"ar": 17},
        "khazin": {"ar": 18},
        "abuhayyan": {"ar": 19},
        "ibnarafa": {"ar": 20},
        "nisaboori": {"ar": 22},
        "tha'alibi": {"ar": 23},
        "ibnaadel": {"ar": 24},
        "baqa'i": {"ar": 25},
        "suyuti": {"ar": 26},
        "abualsoud": {"ar": 28},
        "tustari": {"ar": 29, "en": 93},
        "salami": {"ar": 30},
        "qurayshi": {"ar": 31},
        "baqli": {"ar": 32},
        "ibnarabi": {"ar": 33},
        "ismailhaqqi": {"ar": 36},
        "ibn'ajiba": {"ar": 37},
        "alqimmi": {"ar": 38},
        "tusi": {"ar": 39},
        "sherazi": {"ar": 40},
        "kashani": {"ar": 41, "en": 107},
        "janabidi": {"ar": 42},
        "hubari": {"ar": 44},
        "furatalkufi": {"ar": 45},
        "a'qam": {"ar": 47},
        "hawari": {"ar": 48},
        "hamayan": {"ar": 49},
        "altufaysh": {"ar": 50},
        "khalili": {"ar": 51},
        "alousi": {"ar": 52},
        "sayyidqutb": {"ar": 53},
        "ibnashur": {"ar": 54},
        "shinqiti": {"ar": 55},
        "tabtaba'i": {"ar": 56},
        "tantawi": {"ar": 57},
        "wahidi": {"ar": 60, "en": 86},
        "muntakhab": {"ar": 65},
        "jaza'iri": {"ar": 66},
        "muqatil": {"ar": 67},
        "qattan": {"ar": 68},
        "houmad": {"ar": 71},
        "tha'labi": {"ar": 75},
        "sha'rawi": {"ar": 76},
        "mujahid": {"ar": 78},
        "halabi": {"ar": 79},
        "sabuni": {"ar": 83},
        "sabunimukhtasar": {"ar": 84},
        "sabuniahkam": {"ar": 85},
        "gharnati": {"ar": 88},
        "ibnali": {"ar": 89},
        "andalusi": {"ar": 90},
        "tabarani": {"ar": 91},
        "makki": {"ar": 92},
        "maturidi": {"ar": 94},
        "jilani": {"ar": 95},
        "hashiyajalalayn": {"ar": 96},
        "ibnomar": {"ar": 97},
        "sa'di": {"ar": 98},
        "thawri": {"ar": 99},
        "nasa'i": {"ar": 100},
        "san'ani": {"ar": 101},
        "qasimi": {"ar": 102},
        "mohammadredha": {"ar": 103},
        "ibnabizamneen": {"ar": 104},
        "sajestani": {"ar": 105},
        "ibnaljawzighareeb": {"ar": 106},
        "bahrani": {"ar": 110},
        "rasa'ni": {"ar": 111},
        "kazrouni": {"ar": 112},
        "ibnabbas": {"en": 73},
        "qushayri": {"en": 108},
        "kashf": {"en": 109},
    }

    def is_supported(self, tafsir, language):
        return language in self._tafsirs.get(tafsir)

    def get_url(self, req, tafsir, language):
        language_id = self._languages[language]
        tafsir_id = self._tafsirs[tafsir][language]

        request = req.split(':')
        surah_num = int(request[0])
        ayah_num = int(request[1])

        return self._url.format(
            language_id=language_id,
            tafsir_id=tafsir_id,
            surah_num=surah_num,
            ayah_num=ayah_num)

    def parse(self, response):
        soup = bs4.BeautifulSoup(response, "html.parser")

        ayah_text, tafsir_text = extract_text(soup)
        tafsir_name = soup.find("select", {"id": "Tafsir"}).find("option", {"selected": lambda x: x == ""}).text
        surah_name = soup.find("select", {"id": "SoraName"}).find("option", {"selected": ""}).text.split()[1]

        return TafsirData(ayah_text, tafsir_text, tafsir_name, surah_name)

    def tafsirs(self):
        return self._tafsirs.keys()

    def languages(self):
        return self._languages.keys()
