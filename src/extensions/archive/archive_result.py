from attr import dataclass


@dataclass
class ArchiveResult:
    link: str
    archive_date: str
    cache_hit: bool
