from dataclasses import dataclass
import abc


@dataclass
class TafsirData:
    ayah_text: str
    tafsir_text: str
    tafsir_name: str
    surah_name: str


class TafsirHandler(abc.ABC):
    @abc.abstractmethod
    def is_supported(self, tafsir, language) -> bool:
        pass

    @abc.abstractmethod
    def tafsirs(self):
        pass

    @abc.abstractmethod
    def languages(self):
        pass

    @abc.abstractmethod
    def get_url(self, req, tafsir, language) -> str:
        pass

    @abc.abstractmethod
    def parse(self, response) -> TafsirData:
        pass
