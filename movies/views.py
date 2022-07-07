import json
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from movies.serialize.movie_serializer import MovieSerializer, SearchMovieSerializer
from movies.service.movie_service import MovieService
from movies.model.search_model import SearchLogModel
from movies.serialize.serach_log_serializer import SearchLogSerializer

def first_view(request):
    return render(request, 'default_url.html')


class MoviesListApiView(ListAPIView):
    serializer_class = None
    pagination_class = None
    movies_response = openapi.Response('''Returns information on the number 
                                       of results obtained according to the search, 
                                       most frequent actors and best rated titles''',
                                       SearchMovieSerializer(context={'hits por año': {'2000': '1', '2001': '2'}}))

    name = openapi.Parameter('name', openapi.IN_QUERY,
                             description="Title to search", type=openapi.TYPE_STRING)
    year_start = openapi.Parameter('year_start', openapi.IN_QUERY,
                                   description="Initial year of search", type=openapi.TYPE_INTEGER)
    year_end = openapi.Parameter('year_end', openapi.IN_QUERY,
                                 description="End year of the search", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        operation_description=""" Get movie information from the top 5 
                     in actors and titles of the search selection.
                     """,
        manual_parameters=[name, year_start, year_end],
        responses={204 : 'Error HTTP 204 No Content', 200: movies_response})
    def get(self, request):
        serializer = MovieSerializer(data=self.request.query_params)
        if serializer.is_valid(raise_exception=True):
            movieService = MovieService()
            result = movieService.getInfoMovieByRange(
                search=self.request.query_params["name"],
                year_start=self.request.query_params["year_start"],
                year_end=self.request.query_params["year_end"]
            )
            if result : 
                jsonStr = json.dumps(result.__dict__)
                response_service = Response(jsonStr)
                return response_service
            else :
                content = {'No Content': 'Error HTTP 204 No Content'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

                


class SearchLogListApiView(ListAPIView):
    queryset = SearchLogModel.objects.all()
    serializer_class = SearchLogSerializer
    pagination_class = PageNumberPagination
    
