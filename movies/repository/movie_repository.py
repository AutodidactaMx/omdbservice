import requests
import json
import movies.util.deco_retry as deco_retry
from movies.util.generic import get_total_pages
from omdbservice.settings import REQUEST_API, API_KEYS
from movies.exceptions.custom_error import OmdbapiException


class MovieRepositoryApi:

    def __init__(self) -> None:
        self.url: str = REQUEST_API
        self.keys_tmp: list = API_KEYS.copy()
        self.apikey = self.get_keys()
        self.countRequest = 0

    def get_keys(self):
        if len(self.keys_tmp) == 0:
            self.keys_tmp = API_KEYS.copy()
        key = self.keys_tmp.pop()
        return key

    def get_movies_by_range_year(self, search: str, year_start: int, year_end: int):
        movies = []
        for year in range(int(year_start), int(year_end) + 1, 1):
            json_object = self.__request_data(year=year, search=search)
            for page in range(1, get_total_pages(json_object=json_object) + 1):
                json_movies = self.__request_data(
                    year=year, search=search, page=page)
                if "Search" in json_movies:
                    values = json_movies["Search"]
                    for value in values:
                        movie = self.__request_data(
                            year=year, imdbID=value["imdbID"], page=page)
                        if "imdbRating" in movie:
                            movie["imdbRating"] = float(movie["imdbRating"]) * 100 if movie[
                                                                                          "imdbRating"] != 'N/A' else 0.0
                        movies.append(movie)

        return movies

    @deco_retry.retry(OmdbapiException, tries=6)
    def __request_data(self, year: int, imdbID: str = None, search: str = None, page: int = 1):
        self.countRequest += 1
        payload = {}
        headers = {}
        url = f"{self.url}?apikey={self.apikey}&y={year}&page={page}"
        if search:
            url = f"{url}&s={search}"
        if imdbID:
            url = f"{url}&i={imdbID}"
        response = requests.request("GET", url, headers=headers, data=payload)
        if self.countRequest == 3:
            self.countRequest = 0
            self.apikey = self.get_keys()
        if response.status_code == 401:
            self.apikey = self.get_keys()
            raise OmdbapiException(f"apikey {self.apikey}")
        elif response.status_code != 200:
            self.apikey = self.get_keys()
            raise Exception("Error General")

        return json.loads(response.text)


class MovieRepository(MovieRepositoryApi):
    def __init__(self) -> None:
        super().__init__()
