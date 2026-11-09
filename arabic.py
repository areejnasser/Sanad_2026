"""Arabic text helpers: normalise what the user said and find the object."""
import re
from config import OBJECTS

_DIACRITICS = re.compile(r"[ً-ْـ]")   # tashkeel + tatweel


def normalize(text: str) -> str:
    """Make Arabic spelling consistent so matching is simple."""
    text = _DIACRITICS.sub("", text)
    text = re.sub("[إأآ]", "ا", text)
    text = text.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    text = re.sub(r"[^\w\s]", " ", text)                 # remove punctuation like ؟ ،
    return re.sub(r"\s+", " ", text).strip()


def find_object(question: str):
    """Return the object key (e.g. "glasses") mentioned in the question, or None."""
    q = normalize(question)
    best, best_len = None, 0
    for key, info in OBJECTS.items():
        for kw in info["keywords"]:
            kw_n = normalize(kw)
            if kw_n in q and len(kw_n) > best_len:      # longest match wins
                best, best_len = key, len(kw_n)
    return best
