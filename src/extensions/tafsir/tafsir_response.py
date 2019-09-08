import bs4
from bs4 import Tag, NavigableString


class TafsirResponse:
    def __init__(self, response):
        soup = bs4.BeautifulSoup(response, "html.parser")
        self.text = self.extract_text(soup)

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

        return text.get_text()



