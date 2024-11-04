# deck.py

import random

# Clase para representar una carta
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        # Ajustar la ruta para que apunte a la carpeta correcta
        self.image_filename = f"Pokeran/static/img/cards/{rank}_of_{suit}.png"

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    # def to_dict(self):
    #     return {"rank": self.rank, "suit": self.suit, "image_filename": self.image_filename}

    def to_dict(self):
        return {
            "rank": self.rank,
            "suit": self.suit,
            "image_filename": self.image_filename
        }

# Clase para representar la baraja
class Deck:
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

    # Inicializa y baraja el mazo automáticamente
    # def __init__(self):
    #     self.cards = [Card(rank, suit) for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]
    #                   for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]
    #     random.shuffle(self.cards)

    # def __init__(self):
    #     self.cards = [{'rank': rank, 'suit': suit} for suit in self.suits for rank in self.ranks]
    #     random.shuffle(self.cards)  # Baraja las cartas al crear la instancia

    # Inicializa y baraja el mazo automáticamente
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.shuffle()  # Baraja las cartas al crear la instancia

    def shuffle(self):
        random.shuffle(self.cards)

    # def deal(self, num_cards):
    #     if num_cards > len(self.cards):
    #         raise ValueError("No hay suficientes cartas en la baraja.")
    #     dealt_cards = self.cards[:num_cards]
    #     self.cards = self.cards[num_cards:]
    #     return [{"rank": card.rank, "suit": card.suit, "image_filename": card.image_filename} for card in dealt_cards]

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("No hay suficientes cartas en la baraja.")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return [card.to_dict() for card in dealt_cards]  # Convertir a dict para fácil manejo en el front

    def reset(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    def remaining_cards(self):
        return len(self.cards)

    def __len__(self):
        return len(self.cards)
    
    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"

    