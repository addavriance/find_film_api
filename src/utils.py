from src.swears import SFilter


def has_swear(sf: SFilter, text: str) -> bool:
    return sf.regex_check(text) or sf.fuzzy_check(text) or sf.neural_check(text)