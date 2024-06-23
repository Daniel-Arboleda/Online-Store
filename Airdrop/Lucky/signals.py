# Lucky/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser, Wallet

# @receiver(post_save, sender=CustomUser)
# def create_wallet_for_user(sender, instance, created, **kwargs):
#     """
#     Crea automáticamente una billetera para un usuario recién creado.
#     """
#     if created:
#         Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})
#         print(f"Wallet created for user: {instance.email}")  # Mensaje de depuración
#     else:
#         print(f"User updated: {instance.email}")  # Mensaje de depuración para actualización


# # Conectar la señal post_save para crear automáticamente una billetera cuando se crea un usuario
# post_save.connect(create_wallet_for_user, sender=CustomUser)




@receiver(post_save, sender=CustomUser)
def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
    """
    Crea automáticamente una billetera y un carrito de compras para un usuario recién creado.
    """
    if created:
        Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})
        Cart.objects.get_or_create(user=instance)
        print(f"Wallet and Shopping Cart created for user: {instance.email}")  # Mensaje de depuración
    else:
        print(f"User updated: {instance.email}")  # Mensaje de depuración para actualización

# Conectar la señal post_save para crear automáticamente una billetera y un carrito cuando se crea un usuario
post_save.connect(create_wallet_and_cart_for_user, sender=CustomUser)