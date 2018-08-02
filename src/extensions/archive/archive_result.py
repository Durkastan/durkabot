class ArchiveResult:
    def __init__(self, link, archive_date, cache_hit):
        self.link = link
        self.archive_date = archive_date
        self.cache_hit = cache_hit

    def __repr__(self):
        return (f"ArchiveResult("
                f"link='{self.link}', "
                f"archive_date='{self.archive_date}', "
                f"cache_hit={self.cache_hit}"
                f")")

    # TODO: DRY with BookData
    def __eq__(self, other):
        ret = True
        # ensure member variables are equal
        for k in [x for x, y in self.__dict__.items() if not x.startswith('_') or callable(y)]:
            ret = ret and getattr(self, k) == getattr(other, k)

        return ret

    def __ne__(self, other):
        return not self.__eq__(other)
