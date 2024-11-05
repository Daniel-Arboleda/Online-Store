
# Pokeran/views.py

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction, models
from django.core.exceptions import ObjectDoesNotExist
from Lucky.models import Wallet
from flask import jsonify
from .models import Wallet
from .deck import Deck
from .models import Game
import logging
import json


# Configuración de logger
logger = logging.getLogger('django')
logging.basicConfig(filename="debug.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

@login_required
def play_view(request):
    logger.debug("Iniciando la vista play_view")
    game, created = Game.objects.get_or_create(
        user_email=request.user.email,
        status='active',
        defaults={'player_name': request.user.email}
    )

    try:
        wallet = Wallet.objects.using('default').get(user=request.user)
        balance = wallet.amount
        logger.info(f"Billetera encontrada para el usuario {request.user.email}: Balance {balance}")
    except Wallet.DoesNotExist:
        logger.error(f"No se encontró billetera para el usuario: {request.user.email}")
        balance = 0

    if created or not game.player_hand:
        from .deck import Deck
        deck = Deck()
        player_hand = deck.deal(5)
        game.player_hand = player_hand
        game.save()
    else:
        player_hand = game.player_hand

    logger.debug(f"Datos enviados a la plantilla play.html: game={game}, player_hand={player_hand}, balance={balance}")
    return render(request, 'pokeran/play.html', {'game': game, 'player_hand': player_hand, 'balance': balance})

# @csrf_exempt
# @require_POST
# def update_balance(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             new_balance = data.get('balance')
#             request.user.wallet.amount = new_balance
#             request.user.wallet.save()
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             logger.error(f"Error al actualizar el balance: {e}")
#             return JsonResponse({'status': 'error', 'message': str(e)})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=403)

@csrf_exempt
@require_POST
def update_balance(request):
    try:
        data = json.loads(request.body)
        new_balance = data.get('balance')
        logger.debug(f"Datos recibidos en update_balance: {data}")

        request.user.wallet.amount = new_balance
        request.user.wallet.save()
        logger.info(f"Balance actualizado para {request.user.email}: {new_balance}")


        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error al actualizar el balance: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def show_hand(request, game_id):
    """Muestra las manos de un juego específico."""
    game = get_object_or_404(Game, id=game_id)
    hands = game.hands.all()
    return render(request, 'pokeran/hand.html', {'game': game, 'hands': hands})

def start_game(request):
    # lógica de la vista
    return render(request, 'pokeran/start_game.html')

def get_player_hand(request):
    if request.method == 'GET':
        # Supongamos que tienes un objeto de sesión que mantiene la mano del jugador
        player_hand = request.session.get('player_hand', [])
        balance = request.session.get('balance', 1500)
        jackpot = request.session.get('jackpot', 30000)

        data = {
            "player_hand": player_hand,
            "balance": int(balance),
            "jackpot": int(jackpot)
        }
        logger.debug(f"Datos de la mano del jugador enviados: {data}")
        logger.debug("Datos enviados como respuesta: %s", data)
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

# @login_required
# @csrf_exempt
# def deal_new_hand(request):
#     if request.method == 'GET':
#         try:
#             deck = Deck()
#             new_hand = deck.deal(5)
#             return JsonResponse({'hand': new_hand})
#         except Exception as e:
#             logger.error(f"Error al repartir cartas: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

# @login_required
# @csrf_exempt
# @require_POST
# def deal_new_hand(request):
#     if request.method == 'POST':  # Cambia a POST para mayor consistencia en modificar datos
#         try:
#             deck = Deck()  # Inicializa una baraja de cartas
#             new_hand = deck.deal(5)  # Genera una nueva mano de 5 cartas
#             return JsonResponse({'hand': new_hand})
#         except Exception as e:
#             logger.error(f"Error al repartir cartas: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
@csrf_exempt
@require_POST
def deal_new_hand(request):
    try:
        deck = Deck()
        new_hand = deck.deal(5)
        return JsonResponse({'hand': new_hand})
    except Exception as e:
        logger.error(f"Error al repartir cartas: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)



def deal_cards(request, num_cards):
    deck = Deck()  # Crea una baraja y la baraja automáticamente
    hand = deck.deal(num_cards)  # Reparte la cantidad de cartas necesarias
    return JsonResponse(hand, safe=False)  # Retorna las cartas como JSON

@login_required
@transaction.atomic
def procesar_transaccion(request):
    user = request.user
    amount = request.POST.get('amount')

    try:
        # Bloquea el monto al leer para evitar cambios concurrentes
        wallet = Wallet.objects.select_for_update().get(user=user)
        
        # Actualiza la billetera
        wallet.amount = models.F('amount') + amount
        wallet.save(update_fields=['amount', 'last_update_date'])

        # Validación adicional para garantizar integridad
        transaction_instance = Transaction(
            user=user,
            wallet=wallet,
            ip_address=request.META.get('REMOTE_ADDR'),
            amount=amount
        )
        transaction_instance.save()
    except ObjectDoesNotExist:
        # Manejo si la billetera no existe
        logger.error("No wallet found for user.")
    except Exception as e:
        # Logger para excepciones específicas y rollback
        transaction.rollback()
        logger.error(f'Error processing transaction: {str(e)}')