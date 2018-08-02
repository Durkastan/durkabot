from unittest.mock import MagicMock

import pytest

from extensions.booksearch.bookdata import BookData
from extensions.booksearch.booksite import BookSite, UnSupportedSite
from extensions.booksearch.handlers import WaqfeyaHandler


def test_init(ctx):
    b = BookSite(MagicMock(spec=ctx), MagicMock(spec=WaqfeyaHandler))

    assert b is not None
    assert b.handler is not None


@pytest.mark.asyncio
async def test_convert_returns_object_if_supported_site(ctx):
    site = 'waqfeya'

    assert isinstance(await BookSite.convert(MagicMock(spec=ctx), site), BookSite)


@pytest.mark.asyncio
async def test_convert_raises_error_if_not_supported_site(ctx):
    site = 'nonexistentlibrary'

    with pytest.raises(UnSupportedSite):
        await BookSite.convert(MagicMock(spec=ctx), site)


@pytest.mark.asyncio
async def test_search_returns_embed_with_results(ctx):
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
                 link="https://archive.org/download/FP99429/99429.pdf", site_link="book.php?bid=9849"),
        BookData(title='test book 1', author_name=None, link='uncle-google.com', site_link='also-uncle-google.com'),
        BookData(title='test book 2', author_name='some dude', link=None, site_link='uncle-google.com'),
        BookData(title='test book 3', author_name='some other dude', link='uncle-google.com', site_link=None)
    ]
    search_url = 'uncle-google.com'
    b = BookSite(MagicMock(spec=ctx), MagicMock(spec=WaqfeyaHandler))

    async def search(query, tag):
        return bookls, search_url

    b.handler.search = search
    b.handler.format_result = WaqfeyaHandler.format_result

    embed = await b.search('fake query', None)

    for index, field in enumerate(embed.fields):
        book = bookls[index]

        assert book.title == field.name
        if book.author_name is not None:
            assert book.author_name in field.value
        if book.link is not None:
            assert book.link in field.value
        if book.site_link is not None:
            assert book.site_link in field.value
