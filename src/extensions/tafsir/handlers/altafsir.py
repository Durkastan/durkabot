from aiohttp import ClientSession

import bs4
from bs4 import Tag, NavigableString
from discord.ext.commands import BadArgument


class AlTafsir:
    def __init__(self, loop):
        self.session = ClientSession(loop=loop)

    async def fetch(self, req, tafsir, language):
        request = TafsirRequest(req, tafsir, language)

        async with self.session.get(request.url) as r:
            response = await r.text()

        return TafsirResponse(response), request.url


class TafsirRequest:
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
        "ar": {
            "tabari": 1,
            "zamakhshari": 2,
            "tabrasi": 3,
            "razi": 4,
            "qurtubi": 5,
            "baydawi": 6,
            "ibnkathir": 7,
            "jalalayn": 8,
            "shawkani": 9,
            "fairuzabadi": 10,
            "samarqandi": 11,
            "mawardi": 12,
            "baghawi": 13,
            "ibnattiyah": 14,
            "ibnaljawzi": 15,
            "ibnabdalsalam": 16,
            "nasafi": 17,
            "khazin": 18,
            "abuhayyan": 19,
            "ibnarafa": 20,
            "nisaboori": 22,
            "tha'alibi": 23,
            "ibnaadel": 24,
            "baqa'i": 25,
            "suyuti": 26,
            "abualsoud": 28,
            "tustari": 29,
            "salami": 30,
            "qurayshi": 31,
            "baqli": 32,
            "ibnarabi": 33,
            "ismailhaqqi": 36,
            "ibn'ajiba": 37,
            "alqimmi": 38,
            "tusi": 39,
            "sherazi": 40,
            "kashani": 41,
            "janabidi": 42,
            "hubari": 44,
            "furatalkufi": 45,
            "a'qam": 47,
            "hawari": 48,
            "hamayan": 49,
            "altufaysh": 50,
            "khalili": 51,
            "alousi": 52,
            "sayyidqutb": 53,
            "ibnashur": 54,
            "shinqiti": 55,
            "tabtaba'i": 56,
            "tantawi": 57,
            "wahidi": 60,
            "muntakhab": 65,
            "jaza'iri": 66,
            "muqatil": 67,
            "qattan": 68,
            "houmad": 71,
            "tha'labi": 75,
            "sha'rawi": 76,
            "mujahid": 78,
            "halabi": 79,
            "sabuni": 83,
            "sabunimukhtasar": 84,
            "sabuniahkam": 85,
            "gharnati": 88,
            "ibnali": 89,
            "andalusi": 90,
            "tabarani": 91,
            "makki": 92,
            "maturidi": 94,
            "jilani": 95,
            "hashiyajalalayn": 96,
            "ibnomar": 97,
            "sa'di": 98,
            "thawri": 99,
            "nasa'i": 100,
            "san'ani": 101,
            "qasimi": 102,
            "mohammadredha": 103,
            "ibnabizamneen": 104,
            "sajestani": 105,
            "ibnaljawzighareeb": 106,
            "bahrani": 110,
            "rasa'ni": 111,
            "kazrouni": 112,
        },
        "en": {
            "ibnabbas": 73,
            "jalalayn": 74,
            "wahidi": 86,
            "tustari": 93,
            "kashani": 107,
            "qushayri": 108,
            "kashf": 109,
        }
    }

    def __init__(self, req, tafsir, language):
        if language not in self._languages:
            raise BadArgument("Invalid language! Supported languages are: `en`, `ar`")
        if tafsir not in self._tafsirs[language]:
            if tafsir in self._tafsirs["ar" if language == "en" else "en"]:
                language = "ar" if language == "en" else "en"
            else:
                supported_tafsirs = str(list(self._tafsirs[language].keys())).strip('[]').replace('"', "").replace(",", "")
                raise BadArgument(f"Invalid tafsir! Supported {language} tafsirs are: {supported_tafsirs}")

        self.language_id = self._languages[language]
        self.tafsir_id = self._tafsirs[language][tafsir]

        request = req.split(':')
        self.surah_num = int(request[0])
        self.ayah_num = int(request[1])

    @property
    def url(self):
        return self._url.format(
            language_id=self.language_id,
            tafsir_id=self.tafsir_id,
            surah_num=self.surah_num,
            ayah_num=self.ayah_num)


class TafsirResponse:
    def __init__(self, response):
        soup = bs4.BeautifulSoup(response, "html.parser")
        self.ayah_text, self.tafsir_text = self.extract_text(soup)
        self.tafsir_name = soup.find("select", {"id": "Tafsir"}).find("option", {"selected": lambda x: x == ""}).text
        self.surah_name = soup.find("select", {"id": "SoraName"}).find("option", {"selected": ""}).text.split()[1]

    def remove_child(self, parent, child_index):
        child = parent.contents[child_index]
        if isinstance(child, Tag):
            child.decompose()
        elif isinstance(child, NavigableString):
            parent.contents.remove(child)

    def extract_text(self, soup):
        text: Tag = soup.find("div", {'id': "SearchResults"})

        self.remove_child(text, 0)

        subtxt = text.contents[-1]
        self.remove_child(subtxt, -1)

        separator = subtxt.find("hr")
        if separator:
            separator_index = subtxt.contents.index(separator)
            while len(subtxt.contents) - 1 > separator_index:
                self.remove_child(subtxt, separator_index)

        s = text.get_text()
        ind = s.find("}")
        return s[:ind + 1], s[ind + 1:]
