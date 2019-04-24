import re

from bs4 import BeautifulSoup


class HadithResponse:
    def __init__(self, data):
        soup = BeautifulSoup(data, "html.parser")

        arabic_text_raw = soup.find("div", {"class": "arabic_hadith_full arabic"}).text
        self.arabic_text = self.format_hadith_text(arabic_text_raw)

        english_text_raw = soup.find("div", {"class": "text_details"}).text
        self.english_text = self.format_hadith_text(english_text_raw)

        self.grading = self.element_text_or_none(soup, "td", {"class": "english_grade"})
        self.narrator = self.element_text_or_none(soup, "div", {"class": "hadith_narrated"})

        self.chapter_name = self.element_text_or_none(soup, "div", {"class": "arabicchapter arabic"})

        crumbs = soup.find('div', {"class": "crumbs"}).text.split('»')
        self.book_title = crumbs[1]
        self.book_section_name = crumbs[2]

    @staticmethod
    def format_hadith_text(text):
        txt = str(text) \
            .replace('`', '\\`') \
            .replace('\n', '') \
            .replace('<i>', '*') \
            .replace('</i>', '*')

        return re.sub('\s+', ' ', txt)

    @staticmethod
    def element_text_or_none(soup, name, attrs):
        element = soup.find(name, attrs)
        return element.text if element is not None else ''
