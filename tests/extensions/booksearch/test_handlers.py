from unittest.mock import MagicMock

import pytest
from bs4 import BeautifulSoup

from extensions.booksearch.bookdata import BookData
from extensions.booksearch.handlers import WaqfeyaHandler


class TestWaqfeyaHandler:
    def test_init(self, ctx):
        wh = WaqfeyaHandler(MagicMock(spec=ctx))

        assert wh.session is not None

    def test_process_result_parses_tag_and_returns_bookdata(self):
        # list of 15 results on the sample page; static input should give static output.
        bookls = [
            BookData(title="صحيح البخاري (ت: ابن أبي علفة)",
                     author_name="محمد بن إسماعيل بن إبراهيم البخاري أبو عبد الله",
                     link="https://archive.org/details/FP154296", site_link="book.php?bid=12247"),
            BookData(title="القول الفريد فوائد على كتاب التوحيد", author_name="زيد بن مسفر البحري",
                     link="https://archive.org/download/FP163674/163674.pdf", site_link="book.php?bid=12218"),
            BookData(title="صحيح البخاري (ط. الأوقاف السعودية)",
                     author_name="محمد بن إسماعيل بن إبراهيم البخاري أبو عبد الله",
                     link="https://archive.org/download/FP34714/34714.pdf", site_link="book.php?bid=12205"),
            BookData(title="أضواء السنة", author_name="عبد الله بن عبد العزيز بن محمد اللحيدان",
                     link="https://archive.org/download/FP160479/160479.pdf", site_link="book.php?bid=12004"),
            BookData(title="المنهل الحديث في شرح الحديث", author_name="موسى شاهين لاشين",
                     link="https://archive.org/download/FP56908/01_56908.pdf", site_link="book.php?bid=11864"),
            BookData(title="صحيح البخاري (الكتاب الصوتي)", author_name="محمد بن إسماعيل بن إبراهيم بن المغيرة البخاري",
                     link="https://archive.org/download/Sahih_Al-Bukhari_MP3/Sahih_Al-Bukhari_01.mp3",
                     site_link="book.php?bid=11726"),
            BookData(title="كتاب التوحيد وكتاب القول السديد في مقاصد التوحيد",
                     author_name="محمد بن عبد الوهاب - عبد الرحمن بن ناصر السعدي",
                     link="https://archive.org/details/FP26444",
                     site_link="book.php?bid=11492"),
            BookData(title="الزيادات على الموضوعات ويسمى ذيل اللآلئ المصنوعة",
                     author_name="جلال الدين عبد الرحمن بن أبي بكر السيوطي",
                     link="https://archive.org/details/FP113273", site_link="book.php?bid=11336"),
            BookData(title="مجموع مؤلفات الشيخ العلامة عبد الرحمن بن ناصر السعدي (ط. الأوقاف القطرية)",
                     author_name="عبد الرحمن بن ناصر السعدي",
                     link="https://archive.org/download/FP121941/01_121941.pdf", site_link="book.php?bid=11206"),
            BookData(title="المهذب من إحياء علوم الدين", author_name="صالح أحمد الشامي",
                     link="https://archive.org/download/FP9886/01_9886.pdf", site_link="book.php?bid=10922"),
            BookData(title="المحلى بالآثار (ط. العلمية)", author_name="علي بن أحمد بن سعيد بن حزم الأندلسي أبو محمد",
                     link="https://archive.org/details/FP74771", site_link="book.php?bid=10863"),
            BookData(title="مشكل الحديث وبيانه", author_name="ابن فورك",
                     link="https://archive.org/details/mshabimshabi", site_link="book.php?bid=10733"),
            BookData(title="التذكرة في الفقه الشافعي",
                     author_name="عمر بن علي بن أحمد بن محمد المصري ابن الملقن الشافعي",
                     link="https://archive.org/details/FP89691", site_link="book.php?bid=10622"),
            BookData(title="الموضوعات", author_name="عبد الرحمن بن علي بن محمد بن علي بن الجوزي أبو الفرج",
                     link="https://archive.org/details/FP15210", site_link="book.php?bid=10599"),
            BookData(title="السراج المنير في ترتيب أحاديث صحيح الجامع الصغير", author_name="عصام موسى هادي",
                     link="https://archive.org/download/FP99429/99429.pdf", site_link="book.php?bid=9849")
        ]

        with open('res/search_sample.html', 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        results = soup.find_all('span', attrs={'class': 'postbody'})[2:-1]

        for index, result in enumerate(results):
            bookdata = WaqfeyaHandler.process_result(result)
            assert bookdata == bookls[index]

    @pytest.mark.asyncio
    async def test_search_searches_query(self, ctx):
        test_table = {  # (query, tag): url
            ('صحيح البخاري', ''): 'http://waqfeya.com/search.php?getword=صحيح البخاري&field=btags',
            ('سنن النسائي', 'title'): 'http://waqfeya.com/search.php?getword=سنن النسائي&field=btitle',
            ('الترمذي', 'author'): 'http://waqfeya.com/search.php?getword=الترمذي&field=athid',
            ('رائد', 'verifier'): 'http://waqfeya.com/search.php?getword=رائد&field=verid',
            ('ابو داود', 'card'): 'http://waqfeya.com/search.php?getword=ابو داود&field=binfo',
            ('ابن ماجة', 'toc'): 'http://waqfeya.com/search.php?getword=ابن ماجة&field=btoc',
            ('صحيح مسلم', 'tags'): 'http://waqfeya.com/search.php?getword=صحيح مسلم&field=btags',
        }

        with open('res/search_sample.html', 'r', encoding='utf-8') as f:
            sample = f.read()

        for (query, tag), expected_url in test_table.items():

            async def _fetch(url):
                assert url == expected_url
                return BeautifulSoup(sample, 'html.parser')

            wh = WaqfeyaHandler(MagicMock(spec=ctx))
            wh._fetch = _fetch

            results = await wh.search(query, tag)
            assert results is not None

            for result in results:
                assert result is not None
                assert isinstance(result, BookData)

