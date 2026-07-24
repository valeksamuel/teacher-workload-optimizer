import json
from pathlib import Path


class Translator:
    def __init__(self, language: str = "sk"):
        file = Path(__file__).parent.parent / "locales" / f"{language}.json"

        with open(file, encoding="utf-8") as f:
            self.translations = json.load(f)

    def translate(self, key: str, **kwargs: object) -> str:
        text = self.translations.get(key, key)
        return text.format(**kwargs)


translator = Translator()
translate = translator.translate
