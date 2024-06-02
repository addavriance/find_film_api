import logging
import pytest
from src.swears import SFilter


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


setup_logging()


@pytest.mark.parametrize(
    "text, expected_result",
    [
        ("нуу оооочень крутой блокбастер сука", True),
        ("фильм про человека паука", False),
    ],
)
def test_has_swear(text, expected_result):
    logging.debug(f"Test has_swear with text: {text}")
    sf = SFilter()
    result = sf.regex_check(text) or sf.fuzzy_check(text) or sf.neural_check(text)
    assert result == expected_result
