from django.urls import path
from .views import MovieListAPI

app_name = 'movies'

urlpatterns = [
    path('movies', MovieListAPI.as_view(), name='movie_list')
]
