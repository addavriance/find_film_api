import re
from src.swears import SFilter


def has_swear(sf: SFilter, text: str) -> bool:
    return sf.regex_check(text) or sf.fuzzy_check(text) or sf.neural_check(text)


def get_enclosed_json(json: str):
    pattern = re.compile(r"(?s)\{.*?}")
    match = pattern.search(json)
    if match:
        return match.group(0)
    else:
        return None
