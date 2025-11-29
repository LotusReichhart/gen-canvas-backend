import json
import os
from typing import Dict
from loguru import logger

from .logger import setup_logging

setup_logging()

class I18nService:
    def __init__(self):
        self.locales: Dict[str, Dict[str, str]] = {}
        self.default_lang = "en"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        locales_dir = os.path.join(current_dir, "locales")
        self._load_locales(locales_dir)

    def _load_locales(self, locales_dir: str):
        if not os.path.exists(locales_dir):
            os.makedirs(locales_dir, exist_ok=True)
            return

        for filename in os.listdir(locales_dir):
            if filename.endswith(".json"):
                lang_code = filename.split(".")[0]
                try:
                    with open(os.path.join(locales_dir, filename), "r", encoding="utf-8") as f:
                        self.locales[lang_code] = json.load(f)
                except Exception as e:
                    logger.error(f"Lỗi loading locale {filename}: {e}")

    def translate(self, key: str, lang: str = "en") -> str:
        lang_dict = self.locales.get(lang, self.locales.get(self.default_lang, {}))
        return lang_dict.get(key, key)

i18n = I18nService()