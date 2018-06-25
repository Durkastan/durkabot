from extensions.booksearch.bookdata import BookData


d = {
    'title': 'Sahih Al-Bukhari',
    'author_name': 'Abu Abdullah Muhammad bin Ismael Al-Bukhari',
    'link': 'uncle-google.com',
    'site_link': 'also-uncle-google.com'
}


def test_init():
    b = BookData(**d)

    for k, v in d.items():
        assert getattr(b, k) is not None
        assert getattr(b, k) == v


def test_eq_equal_bookdata_return_true():
    b1 = BookData(**d)
    b2 = BookData(**d)

    assert not b1 != b2
    assert b1 == b2


def test_eq_not_equal_bookdata_return_false():
    b1 = BookData(**d)
    b2 = BookData(**d)
    b2.link = 'not-uncle-google.com'

    assert not b1 == b2
    assert b1 != b2


def test_repr_valid_python_code():
    b1 = BookData(**d)
    b2 = eval(repr(b1))

    assert b1 == b2
