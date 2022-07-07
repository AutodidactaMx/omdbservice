from this import d
from movies.dto.search_movies import SearchMovie
from movies.repository.movie_repository import MovieRepository
from movies.repository.search_log import SearchLogRepository
from movies.dto.search_movies import SearchMovie
from movies.model.search_model import SearchLogModel

import pandas as pd
import numpy as np


class MovieService:
    movieRepository: MovieRepository = None
    searchLogRepository: SearchLogRepository = SearchLogRepository()

    def __init__(self) -> None:
        self.movieRepository = MovieRepository()


        
    def getInfoMovieByRange(self, search: str, year_start: int, year_end: int) ->SearchMovie:
        data = self.movieRepository.getMoviesByRangeYear(
            search=search,
            year_start=year_start,
            year_end=year_end)
        if data :
            df_movies = pd.DataFrame(data)
            df_frequency_actors = self.__getFrequencyActors(df_movies)
            df_top_reted = self.__getTopReted(df_movies)
            df_historical_years = self.__getHistoricalYears(df_movies)
            self.__recordSearh(search=search, year_start=year_start,
                            year_end=year_end, df_movies=df_movies,
                            df_frequency_actors=df_frequency_actors,                           
                            df_historical_years=df_historical_years)
            return SearchMovie(
                frequency_actors=df_frequency_actors["top5"].to_dict(),            
                historical_years=df_historical_years["hits"].to_dict(),
                top_reted=df_top_reted.to_dict(),
            )
        else :
            return None

    def __recordSearh(self, search: str, year_start: int, year_end: int, df_movies,
                      df_frequency_actors: pd.DataFrame,                      
                      df_historical_years: dict):
        mct = self.__getMctRating(df_movies)

        searh_log = SearchLogModel(
            search_parameters={"search": search,
                               "year_start": year_start, "year_end": year_end},
            year_more_results=df_historical_years["max_result"],
            year_less_results=df_historical_years["min_result"],
            actor_more_appearances=df_frequency_actors["max_appearances"],
            actor_less_appearances=df_frequency_actors["min_appearances"],
            rating_min=mct["min"],
            rating_max=mct["max"],
            rating_mean=mct["mean"],
            rating_median=mct["median"],
            rating_std=mct["std"]
        )
        self.searchLogRepository.insert(searh_log=searh_log)

    def __getHistoricalYears(self, movies: pd.DataFrame) -> dict:
        df_hits = movies.groupby("Year")["Year"].count()
        reset = df_hits.reset_index(name='count')
        max_hit = reset.max().to_dict()        
        min_hit = reset.min().to_dict()        
        return {
            "hits": df_hits,
            "max_result": max_hit["Year"],
            "min_result": min_hit["Year"]
        }

    def __getFrequencyActors(self, movies: pd.DataFrame) -> dict:
        df_actors = movies["Actors"]
        split = df_actors.str.split(',')
        stack = pd.DataFrame(split.tolist()).stack()
        dfstack = pd.DataFrame(stack.to_list(), columns=["Actors"])
        dfstackfilter = dfstack[dfstack['Actors'] != "N/A"]
        dfstackcount = dfstackfilter.groupby(['Actors'])['Actors'].agg(
            'count').reset_index(name='count')        
        top = dfstackcount[['Actors', 'count']
                           ].nlargest(n=5, columns=['count'])
        top = top.groupby("Actors")["count"].sum()
        max_appearances = dfstackcount.max().to_dict() 
        min_appearances = dfstackcount.min().to_dict()         
        
        return {
            "top5": top,
            "max_appearances": max_appearances["Actors"],
            "min_appearances": min_appearances["Actors"]
        }
        

    def __getTopReted(self, movies: pd.DataFrame) -> pd.DataFrame:
        filter = movies[["Title", "imdbRating"]].nlargest(
            n=5, columns=['imdbRating'])
        dropDuplicate = filter.drop_duplicates()
        groupby = dropDuplicate.groupby("Title")["imdbRating"].sum()
        return groupby

    def __getMctRating(self, movies: pd.DataFrame) -> dict:
        return {
            "mean": np.mean(movies['imdbRating']),
            "median": np.median(movies['imdbRating']),
            "std": np.std(movies['imdbRating']),
            "max": np.max(movies['imdbRating']),
            "min": np.min(movies['imdbRating']),
        }
