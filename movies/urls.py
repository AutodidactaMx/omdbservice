from django.urls import path,include,re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('v1/', include([
        #path('movies', views.servicio_test, name='api-movies'),    
        path('serachlog', views.SearchLogListApiView.as_view(), name='api-search-log'),
        path('movies', views.MoviesListApiView.as_view(), name='api-movies'),
    ]))       
]

