# pokeran/views.py

from django.shortcuts import render
from .models import Game
from random import shuffle

def otra_vista(request):
    # Lógica de la vista
    return render(request, 'template.html', {})

def pokeran_home(request):
    return render(request, 'pokeran/home.html')

def start_game(request):
    game = Game.objects.create(player_name="Jugador1")
    return render(request, 'pokeran/game.html', {'game': game})

def show_hand(request, game_id):
    game = Game.objects.get(id=game_id)
    hands = game.hands.all()
    return render(request, 'pokeran/hand.html', {'game': game, 'hands': hands})

# Si necesitas usar otra_vista en alguna parte, puedes importarla aquí directamente
