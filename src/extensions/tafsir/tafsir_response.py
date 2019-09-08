import bs4
from bs4 import Tag, NavigableString


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
