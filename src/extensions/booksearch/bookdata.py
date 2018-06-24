class BookData:
    def __init__(self, title, author_name, link, site_link):
        self.title = title
        self.author_name = author_name
        self.link = link
        self.site_link = site_link

    def __repr__(self):
        return (f'BookData('
                f'title="{self.title}", '
                f'author_name="{self.author_name}", '
                f'link="{self.link}", '
                f'site_link="{self.site_link}"'
                f')')

    def __eq__(self, other):
        ret = True
        # ensure member variables are equal
        for k in [x for x, y in self.__dict__.items() if not x.startswith('_') or callable(y)]:
            ret = ret and getattr(self, k) == getattr(other, k)

        return ret

    def __ne__(self, other):
        return not self.__eq__(other)
