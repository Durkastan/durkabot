from aiohttp import ClientSession

from extensions.quran.quraneditions import parse_editions
from extensions.quran.quranrequest import QuranRequest
from extensions.quran.quranresponse import QuranResponse


class QuranFetcher:
    def __init__(self, loop):
        self.session = ClientSession(loop=loop)

    async def fetch(self, req, edition):
        return await self._fetch(QuranRequest(req, edition))

    async def _fetch(self, request):
        async with self.session.get(request.url) as r:
            response = await r.json()
        return QuranResponse(response)

    async def editions(self, language):
        return await self._editions(f'http://api.alquran.cloud/edition?language={language}&format=text')

    async def _editions(self, url):
        async with self.session.get(url) as r:
            response = await r.json()
        return parse_editions(response)
