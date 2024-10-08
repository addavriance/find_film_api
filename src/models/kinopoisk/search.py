import requests

from src.models.kinopoisk.variables import url, eHeaders, eQuery


class Search:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = eHeaders

    def get_film_data(self, film_name: str):

        query = eQuery

        query["query"] = film_name

        movies = self.session.get(url, params=query).json()

        print(movies)

        movie = movies["docs"][0]

        return movie