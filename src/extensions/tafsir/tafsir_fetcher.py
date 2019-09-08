from aiohttp import ClientSession

from extensions.tafsir.tafsir_request import TafsirRequest
from extensions.tafsir.tafsir_response import TafsirResponse


class TafsirFetcher:
    def __init__(self, loop):
        self.session = ClientSession(loop=loop)

    async def fetch(self, req, tafsir, language):
        request = TafsirRequest(req, tafsir, language)

        async with self.session.get(request.url) as r:
            response = await r.text()

        return TafsirResponse(response)
