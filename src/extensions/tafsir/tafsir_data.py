from dataclasses import dataclass


@dataclass
class TafsirData:
    ayah_text: str
    tafsir_text: str
    tafsir_name: str
    surah_name: str
