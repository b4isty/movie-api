from django.urls import path
from .views import MovieListAPI, CollectionListCreateAPIView, CollectionUpdateDestroyAPIView

app_name = 'movies'

urlpatterns = [
    path('movies/', MovieListAPI.as_view(), name='movie_list'),
    path('collection/', CollectionListCreateAPIView.as_view(), name='collection_list'),
    path('collection/<uuid:collection_uuid>/', CollectionUpdateDestroyAPIView.as_view(),
         name='collection_update_delete')
]
