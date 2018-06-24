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
        # lists of 15 results on the sample pages; static input should give static output.
        bookls1 = [
            BookData(title="صحيح البخاري (ت: ابن أبي علفة)",
                     author_name="محمد بن إسماعيل بن إبراهيم البخاري أبو عبد الله",
                     link="https://archive.org/details/FP154296", site_link="http://waqfeya.com/book.php?bid=12247"),
            BookData(title="القول الفريد فوائد على كتاب التوحيد", author_name="زيد بن مسفر البحري",
                     link="https://archive.org/details/FP163674", site_link="http://waqfeya.com/book.php?bid=12218"),
            BookData(title="صحيح البخاري (ط. الأوقاف السعودية)",
                     author_name="محمد بن إسماعيل بن إبراهيم البخاري أبو عبد الله",
                     link="https://archive.org/details/FP34714", site_link="http://waqfeya.com/book.php?bid=12205"),
            BookData(title="أضواء السنة", author_name="عبد الله بن عبد العزيز بن محمد اللحيدان",
                     link="https://archive.org/details/FP160479", site_link="http://waqfeya.com/book.php?bid=12004"),
            BookData(title="المنهل الحديث في شرح الحديث", author_name="موسى شاهين لاشين",
                     link="https://archive.org/details/FP56908", site_link="http://waqfeya.com/book.php?bid=11864"),
            BookData(title="صحيح البخاري (الكتاب الصوتي)", author_name="محمد بن إسماعيل بن إبراهيم بن المغيرة البخاري",
                     link="https://archive.org/details/Sahih_Al-Bukhari_MP3",
                     site_link="http://waqfeya.com/book.php?bid=11726"),
            BookData(title="كتاب التوحيد وكتاب القول السديد في مقاصد التوحيد",
                     author_name="محمد بن عبد الوهاب - عبد الرحمن بن ناصر السعدي",
                     link="https://archive.org/details/FP26444", site_link="http://waqfeya.com/book.php?bid=11492"),
            BookData(title="الزيادات على الموضوعات ويسمى ذيل اللآلئ المصنوعة",
                     author_name="جلال الدين عبد الرحمن بن أبي بكر السيوطي",
                     link="https://archive.org/details/FP113273", site_link="http://waqfeya.com/book.php?bid=11336"),
            BookData(title="مجموع مؤلفات الشيخ العلامة عبد الرحمن بن ناصر السعدي (ط. الأوقاف القطرية)",
                     author_name="عبد الرحمن بن ناصر السعدي", link="https://archive.org/details/FP121941",
                     site_link="http://waqfeya.com/book.php?bid=11206"),
            BookData(title="المهذب من إحياء علوم الدين", author_name="صالح أحمد الشامي",
                     link="https://archive.org/details/FP9886", site_link="http://waqfeya.com/book.php?bid=10922"),
            BookData(title="المحلى بالآثار (ط. العلمية)", author_name="علي بن أحمد بن سعيد بن حزم الأندلسي أبو محمد",
                     link="https://archive.org/details/FP74771", site_link="http://waqfeya.com/book.php?bid=10863"),
            BookData(title="مشكل الحديث وبيانه", author_name="ابن فورك",
                     link="https://archive.org/details/mshabimshabi",
                     site_link="http://waqfeya.com/book.php?bid=10733"),
            BookData(title="التذكرة في الفقه الشافعي",
                     author_name="عمر بن علي بن أحمد بن محمد المصري ابن الملقن الشافعي",
                     link="https://archive.org/details/FP89691", site_link="http://waqfeya.com/book.php?bid=10622"),
            BookData(title="الموضوعات", author_name="عبد الرحمن بن علي بن محمد بن علي بن الجوزي أبو الفرج",
                     link="https://archive.org/details/FP15210", site_link="http://waqfeya.com/book.php?bid=10599"),
            BookData(title="السراج المنير في ترتيب أحاديث صحيح الجامع الصغير", author_name="عصام موسى هادي",
                     link="https://archive.org/details/FP99429", site_link="http://waqfeya.com/book.php?bid=9849")]
        bookls2 = [
            BookData(title="شرح أبواب من صحيح البخاري ويليه شرح أبواب من جامع الترمذي", author_name="ابن رجب الحنبلي",
                     link="https://archive.org/details/FP171605", site_link="http://waqfeya.com/book.php?bid=12390"),
            BookData(title="مؤتمر الانتصار للصحيحين", author_name="مجموعة من المؤلفين",
                     link="https://archive.org/details/IntsahIntsahPDF",
                     site_link="http://waqfeya.com/book.php?bid=12262"),
            BookData(title="صحيح البخاري (ت: ابن أبي علفة)",
                     author_name="محمد بن إسماعيل بن إبراهيم البخاري أبو عبد الله",
                     link="https://archive.org/details/FP154296", site_link="http://waqfeya.com/book.php?bid=12247"),
            BookData(title="صحيح البخاري (ط. الأوقاف السعودية)",
                     author_name="محمد بن إسماعيل بن إبراهيم البخاري أبو عبد الله",
                     link="https://archive.org/details/FP34714", site_link="http://waqfeya.com/book.php?bid=12205"),
            BookData(title="البحر الذي زخر في شرح ألفية الأثر", author_name="جلال الدين السيوطي",
                     link="https://archive.org/details/FP61983", site_link="http://waqfeya.com/book.php?bid=12089"),
            BookData(title="فتاوى اللجنة الدائمة للبحوث العلمية والإفتاء (المجموعة الثانية)",
                     author_name="اللجنة الدائمة للبحوث العلمية والإفتاء", link="https://archive.org/details/FP168880",
                     site_link="http://waqfeya.com/book.php?bid=12056"),
            BookData(title="صحيح البخاري الجامع المسند الصحيح المختصر من أمور رسول الله صلى الله عليه وسلم مع حاشية السهارنفوري وحاشية السندي (ط. البشرى)",
                     author_name="محمد بن إسماعيل بن إبراهيم البخاري أبو عبد الله",
                     link="https://archive.org/details/FP163611", site_link="http://waqfeya.com/book.php?bid=11909"),
            BookData(title="الحلل الإبريزية من التعليقات البازية على صحيح البخاري",
                     author_name="عبد العزيز بن عبد الله بن باز - عبد الله بن مانع الروقي أبو محمد",
                     link="https://archive.org/details/FP79821", site_link="http://waqfeya.com/book.php?bid=11868"),
            BookData(title="المجالس الوعظية في شرح أحاديث خير البرية صلى الله عليه وسلم من صحيح الإمام البخاري",
                     author_name="محمد بن عمر بن أحمد السفيري الشافعي", link="https://archive.org/details/FP74768",
                     site_link="http://waqfeya.com/book.php?bid=11867"),
            BookData(title="أزمة البخاري", author_name="معتز عبد الرحمن", link="https://archive.org/details/azmbukPDF",
                     site_link="http://waqfeya.com/book.php?bid=11797"),
            BookData(title="صحيح البخاري (الكتاب الصوتي)", author_name="محمد بن إسماعيل بن إبراهيم بن المغيرة البخاري",
                     link="https://archive.org/details/Sahih_Al-Bukhari_MP3",
                     site_link="http://waqfeya.com/book.php?bid=11726"),
            BookData(title="موسوعة الأعمال الكاملة للإمام محمد الخضر حسين", author_name="محمد الخضر حسين",
                     link="https://archive.org/details/FP125181", site_link="http://waqfeya.com/book.php?bid=11688"),
            BookData(title="صحيح البخاري (ط. العامرة - تركيا)", author_name="محمد بن إسماعيل البخاري",
                     link="https://archive.org/details/FP106658", site_link="http://waqfeya.com/book.php?bid=11645"),
            BookData(title="ثبت أبي جعفر أحمد بن علي البلوي الوادي آشي (ت: العمراني)",
                     author_name="أبو جعفر أحمد بن علي البلوي الوادي آشي",
                     link="https://archive.org/details/tgaabwatgaabwa",
                     site_link="http://waqfeya.com/book.php?bid=11249"),
            BookData(title="موقع موسوعة صحيح البخاري", author_name="موسوعة صحيح البخاري", link=None,
                     site_link="http://waqfeya.com/book.php?bid=11243")
        ]

        test_table = {
            'res/search_sample.html': bookls1,
            'res/search_sample2.html': bookls2
        }

        for filename, bookls in test_table.items():
            with open(filename, 'r', encoding='windows-1256') as f:
                soup = BeautifulSoup(f.read(), 'html.parser', from_encoding='windows-1256')

            results = soup.find_all('span', attrs={'class': 'postbody'})[2:-1]

            wh = WaqfeyaHandler(MagicMock())
            for index, result in enumerate(results):
                bd = wh.process_result(result)
                assert bd is not None
                bd2 = bookls[index]
                assert bd.title == bd2.title
                assert bd.author_name == bd2.author_name
                assert bd.link == bd2.link
                assert bd.site_link == bd2.site_link

    @pytest.mark.asyncio
    async def test_search_searches_query(self, ctx):
        test_table = {
            ('صحيح البخاري', ''): 'http://waqfeya.com/search.php?'
                                  'getword=%D5%CD%ED%CD+%C7%E1%C8%CE%C7%D1%ED&field=btags',
            ('سنن النسائي', 'title'): 'http://waqfeya.com/search.php?'
                                      'getword=%D3%E4%E4+%C7%E1%E4%D3%C7%C6%ED&field=btitle',
            ('الترمذي', 'author'): 'http://waqfeya.com/search.php?getword=%C7%E1%CA%D1%E3%D0%ED&field=athid',
            ('رائد', 'verifier'): 'http://waqfeya.com/search.php?getword=%D1%C7%C6%CF&field=verid',
            ('ابو داود', 'card'): 'http://waqfeya.com/search.php?getword=%C7%C8%E6+%CF%C7%E6%CF&field=binfo',
            ('ابن ماجة', 'toc'): 'http://waqfeya.com/search.php?getword=%C7%C8%E4+%E3%C7%CC%C9&field=btoc',
            ('صحيح مسلم', 'tags'): 'http://waqfeya.com/search.php?getword=%D5%CD%ED%CD+%E3%D3%E1%E3&field=btags'
        }

        with open('res/search_sample.html', 'r', encoding='windows-1256') as f:
            sample = f.read()

        async def _fetch(url):
            return BeautifulSoup(sample, 'html.parser', from_encoding='windows-1256')

        for (query, tag), expected_url in test_table.items():

            wh = WaqfeyaHandler(MagicMock(spec=ctx))
            wh._fetch = _fetch

            results, url = await wh.search(query, tag)
            assert results is not None
            assert url == expected_url

            for result in results:
                assert result is not None
                assert isinstance(result, BookData)

