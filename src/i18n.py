import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Translator:
    def __init__(self, language: str = "sk", strict: bool = False):
        file = Path(__file__).parent.parent / "locales" / f"{language}.json"
        self.strict = strict
        self._reported: set[str] = set()

        try:
            with open(file, encoding="utf-8") as f:
                self.translations: dict[str, str] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error("Failed to load translation file %s: %s", file, e)
            raise

    def translate(self, key: str, default: str | None = None, **kwargs: object) -> str:
        text = self.translations.get(key)

        if text is None:
            if self.strict:
                raise KeyError(f"Missing translation key: {key}")
            if key not in self._reported:
                logger.warning("Missing translation key: %s", key)
                self._reported.add(key)
            text = default if default is not None else f"[[{key}]]"

        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError) as e:
            logger.warning("Bad placeholder %s in translation %r", e, key)
            return text


translator = Translator()
translate = translator.translate
