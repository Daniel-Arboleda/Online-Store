# Pokeran/urls.py




from django.urls import path
from . import views

urlpatterns = [
    path('', views.play_view, name='pokeran_home'),
    path('play/', views.play_view, name='play_view'),
    path('start-game/', views.start_game, name='start_game'),
    path('show_hand/<int:game_id>/', views.show_hand, name='show_hand'),
    path('deal-new-hand/', views.deal_new_hand, name='deal_new_hand'),
    path('api/get_player_hand/', views.get_player_hand, name='get_player_hand'),
    path('update_balance/', views.update_balance, name='update_balance'),
    path('update-balance/', views.update_balance, name='update_balance'),
    path('deal_new_hand/', views.deal_new_hand, name='deal_new_hand'),
]
