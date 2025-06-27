import json
import logging
from pathlib import Path

logger = logging.getLogger("cobalt.i18n")

class i18n:
  def __init__(self, lang_code: str = "en"):
    self.lang_code = lang_code or "en"
    self.translations = self._load_translations()

  def _load_translations(self):
    lang_file = Path(__file__).parent / "locales" / f"{self.lang_code}.json"
    if not lang_file.exists():
      lang_file = Path(__file__).parent / "locales" / "en.json" # fallback to english

    with open(lang_file, "r", encoding="utf-8") as f:
      return json.load(f)

  def get(self, key: str, *args, **kwargs) -> str:
    parts = key.split(".")
    value = self.translations
    for part in parts:
      if isinstance(value, dict):
        value = value.get(part)
        if value is None:
          logging.warning(f"Translation key '{key}' not found.")
          return key
      else:
        logging.warning(f"Translation key '{key}' is not a valid path.")
        return key

    if isinstance(value, str):
      if args or kwargs:
        try:
          return value.format(*args, **kwargs)
        except KeyError as e:
          logging.warning(f"Missing format key {e} in translation for '{key}'")
          return value
        except IndexError as e:
          logging.warning(f"Missing positional argument {e} in translation for '{key}'")
          return value
      else:
        return value
    else:
      logging.warning(f"Value for key '{key}' is not a string.")
      return key