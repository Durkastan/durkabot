from aiohttp import ClientSession

from extensions.quran.quraneditions import parse_editions
from extensions.quran.quranrequest import QuranRequest
from extensions.quran.quranresponse import QuranResponse


class QuranFetcher:
    def __init__(self, loop):
        self.session = ClientSession(loop=loop)

    async def fetch(self, req, edition):
        request = QuranRequest(req, edition)

        async with self.session.get(request.url) as r:
            response = await r.json()

        return QuranResponse(response)

    async def editions(self, language):
        url = f'http://api.alquran.cloud/edition?language={language}&format=text'

        async with self.session.get(url) as r:
            response = await r.json()

        return parse_editions(response)
