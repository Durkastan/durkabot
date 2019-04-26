from aiohttp import ClientSession

from extensions.hadith.hadithresponse import HadithResponse
from extensions.hadith.hadithrequest import get_hadith_request


class HadithFetcher:
    def __init__(self, loop):
        self.session = ClientSession(loop=loop)

    async def fetch(self, book_name, ref):
        return await self._fetch(get_hadith_request(book_name, ref))

    async def _fetch(self, request):
        async with self.session.get(request.url) as r:
            response = await r.read()
        return HadithResponse(response)
