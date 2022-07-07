import requests
import json


class MovieRepositoryApi:
    url: str = None

    def __init__(self) -> None:
        self.url: str = "http://www.omdbapi.com/?apikey=707e914f&?plot=full"

    def __requestData(self, year: int, imdbID: str = None, search: str = None, page: int = 1):
        payload = {}
        headers = {}
        url = f"{self.url}&y={year}&page={page}&plot=full"
        if (search):
            url = f"{url}&s={search}"
        if (imdbID):
            url = f"{url}&i={imdbID}"
        response = requests.request("GET", url, headers=headers, data=payload)
        return json.loads(response.text)

    def __getTotalPages(self, search: str, year: int) -> int:
        json_object = self.__requestData(year=year, search=search)
        print(type(json_object))
        if  "totalResults" in json_object:
            total = int(int(json_object["totalResults"]) / 10) + 1  
        else : 
            total = 0
        return  total

    def getMoviesByRangeYear(self, search: str, year_start: int, year_end: int):
        movies = []
        for year in range(int(year_start), int(year_end)+1, 1):
            for page in range(1, self.__getTotalPages(search=search, year=year)+1):
                json_movies = self.__requestData(
                    year=year, search=search, page=page)
                values = json_movies["Search"]
                for value in values:
                    movie = self.__requestData(
                        year=year, imdbID=value["imdbID"], page=page)                                       
                    movie["imdbRating"] = float(movie["imdbRating"])*100 if movie["imdbRating"] != 'N/A' else 0.0
                    movies.append(movie)
        return movies


class MovieRepository(MovieRepositoryApi):
    def __init__(self) -> None:
        super().__init__()
