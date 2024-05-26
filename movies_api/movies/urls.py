from django.urls import path
from .views import get_movies, get_movies_from_prompt

urlpatterns = [
    path('get_movies/', get_movies, name='get_movies'),
    path('prompt/', get_movies_from_prompt, name='get_movies_from_prompt'),
]

