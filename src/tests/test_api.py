import logging

import pprint
import pytest

from src.constants import MAX_QUERY_LEN


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


pp = pprint.PrettyPrinter(indent=2)

setup_logging()


@pytest.mark.parametrize(
    "query, expected_status_code, expected_data",
    [
        (
            "фильм про человека паука где он смог переходить через вселенные",
            200,
            {
                "film-name": "Человек-паук: Через вселенные",
                "film-autor": "Питер Рэмзи",
                "film-date": "2018",
            },
        ),
    ],
)
def test_search_movie(client, query, expected_status_code, expected_data):
    logging.debug(f"Test search_movie with query: {query}")
    response = client.post("/api/search", json={"query": query})

    logging.debug(f"Status code: {response.status_code}")
    logging.debug(f"Movie data: {pp.pformat(response.json())}")

    assert response.status_code == expected_status_code
    data = response.json()
    assert "film-name" in data
    assert "film-autor" in data
    assert "film-date" in data
    assert "desc" in data

    for key, value in expected_data.items():
        assert value in data[key] or data[key] is None, f"Expected {key}: {value}, got {data[key]}"


@pytest.mark.parametrize(
    "query, expected_status_code, expected_detail",
    [
        ("a" * (MAX_QUERY_LEN + 1), 413, "Query too long."),
        ("нуу оооочень крутой блокбастер сука", 406, "Bad query."),
    ],
)
def test_invalid_query(client, query, expected_status_code, expected_detail):
    logging.debug(f"Test invalid_query with query: {query}")
    response = client.post("/api/search", json={"query": query})

    logging.debug(f"Status code: {response.status_code}")
    logging.debug(f"Detail: {pp.pformat(response.json()['detail'])}")

    assert response.status_code == expected_status_code
    assert response.json() == {"detail": expected_detail}
