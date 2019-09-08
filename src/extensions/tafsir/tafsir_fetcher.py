from aiohttp import ClientSession


class TafsirFetcher:
    def __init__(self, loop):
        self.session = ClientSession(loop=loop)

    def fetch(self, req, tafsir, language):
        pass
