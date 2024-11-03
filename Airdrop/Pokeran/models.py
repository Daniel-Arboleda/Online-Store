# pokeran/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField  # Usar JSONField en Postgres
from Lucky.models import Wallet  # si Wallet está en Lucky/models.py

# from Lucky.wallet_model import Wallet  # si Wallet está en Lucky/wallet_model.py



class Game(models.Model):
    player_name = models.CharField(max_length=255)
    user_email = models.EmailField()  # Almacena el email del usuario autenticado
    player_hand = models.JSONField()  # Almacena las cartas del jugador como JSON
    created_at = models.DateTimeField(auto_now_add=True)
    date_started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('finished', 'Finished')], default='active')
    
    class Meta:
        db_table = 'Game'
        app_label = 'Pokeran'  # Para asegurarse de que el enrutador use la base de datos correcta (pokeran)

    def __str__(self):
        return f"Game for: {self.player_name} - {self.status}"

class Hand(models.Model):
    game = models.ForeignKey(Game, related_name='hands', on_delete=models.CASCADE)
    # cards = models.CharField(max_length=50)  # Representación de las cartas (por ejemplo, 'AS KS 2D 9C 4H')
    cards = models.JSONField()  # Almacena las cartas del jugador como JSON
    result = models.CharField(max_length=100, null=True, blank=True)  # Resultado de la mano

    class Meta:
        db_table = 'Hand'  # Asegúrate de que coincida con la tabla SQL para que coincida el módelo con la tabla personalizada y no use el esquema estandar de Dhjango

    def __str__(self):
        return f"Hand for {self.game.player_name} - {self.result or 'In Progress'}"
