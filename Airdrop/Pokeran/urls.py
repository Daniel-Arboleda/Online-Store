# pokeran/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.pokeran_home, name='pokeran_home'),
    path('start/', views.start_game, name='start_game'),
    path('game/<int:game_id>/', views.show_hand, name='show_hand'),
]
