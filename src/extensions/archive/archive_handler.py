import aiohttp
from urllib.parse import urljoin

from extensions.archive.archive_result import ArchiveResult


class ArchiveHandler:
    archive_org_user_agent = "Durkabot (https://github.com/Durkastan/durkabot)"
    domain = "http://web.archive.org"
    save_url = urljoin(domain, 'save/')

    def __init__(self, loop):
        self.session = aiohttp.ClientSession(loop=loop)

    async def _fetch(self, link, headers):
        async with self.session.get(link, headers=headers) as response:
            await response.read()  # no awaitable method for headers :/
            return response

    async def archive(self, link) -> ArchiveResult:
        request_url = self.save_url + link
        response = await self._fetch(request_url, {'User-Agent': self.archive_org_user_agent})

        # Error handling
        if response.status in [403, 502]:
            raise Exception(response.headers['X-Archive-Wayback-Runtime-Error'])

        archive_result = self.process_result(response.headers)

        return archive_result

    @classmethod
    def process_result(cls, headers):
        archive_id = headers['Content-Location']
        link = urljoin(cls.domain, archive_id)

        # Determine if page is cached
        cache_hit = headers.get('X-Page-Cache') == 'HIT'

        archive_date = headers['X-Archive-Orig-Date']

        return ArchiveResult(link, archive_date, cache_hit)
