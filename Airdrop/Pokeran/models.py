# pokeran/models.py

from django.db import models

class Game(models.Model):
    player_name = models.CharField(max_length=100)
    date_started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('finished', 'Finished')], default='active')
    
    def __str__(self):
        return f"{self.player_name} - {self.status}"

class Hand(models.Model):
    game = models.ForeignKey(Game, related_name='hands', on_delete=models.CASCADE)
    cards = models.CharField(max_length=50)  # Representación de las cartas (por ejemplo, 'AS KS 2D 9C 4H')
    result = models.CharField(max_length=100, null=True, blank=True)  # Resultado de la mano

    def __str__(self):
        return f"Hand for {self.game.player_name} - {self.result or 'In Progress'}"
