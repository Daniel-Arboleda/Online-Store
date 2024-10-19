# Lucky/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser, Wallet, Cart, CartItem, Product
import logging


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




# @receiver(post_save, sender=CustomUser)
# def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
#     """
#     Crea automáticamente una billetera y un carrito de compras para un usuario recién creado.
#     """
#     if created:
#         Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})
#         Cart.objects.get_or_create(user=instance)
#         print(f"Wallet and Shopping Cart created for user: {instance.email}")  # Mensaje de depuración
#     else:
#         print(f"User updated: {instance.email}")  # Mensaje de depuración para actualización

# # Conectar la señal post_save para crear automáticamente una billetera y un carrito cuando se crea un usuario
# post_save.connect(create_wallet_and_cart_for_user, sender=CustomUser)




# @receiver(post_save, sender=CustomUser)
# def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
#     """
#     Crea automáticamente una billetera y un carrito de compras para un usuario recién creado y crea un cartitem por carrito.
#     """
#     if created:
#         Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})
#         cart, created_cart = Cart.objects.get_or_create(user=instance)
#         if created_cart:
#             # Crear un CartItem predeterminado si es necesario
#             CartItem.objects.create(cart=cart, product=Product.objects.first(), quantity=1, price=0)  # Ajusta esto según tus necesidades
#         print(f"Wallet and Shopping Cart created for user: {instance.email}")  # Mensaje de depuración
#     else:
#         print(f"User updated: {instance.email}")  # Mensaje de depuración para actualización

# # Conectar la señal post_save para crear automáticamente una billetera y un carrito cuando se crea un usuario
# post_save.connect(create_wallet_and_cart_for_user, sender=CustomUser)








# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=CustomUser)
# def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
#     """
#     Crea automáticamente una billetera y un carrito de compras para un usuario recién creado y crea un cartitem por carrito.
#     """
#     try:
#         if created:
#             # Crear la billetera
#             Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})

#             cart, created_cart = Cart.objects.get_or_create(user=instance)
#             if created_cart:
#                 # Crear un CartItem predeterminado si es necesario
#                 default_product = Product.objects.first()
#                 if default_product:
#                     CartItem.objects.create(cart=cart, product=default_product, quantity=1, price=0)  # Ajusta esto según tus necesidades
#                 else:
#                     logger.warning(f"No default product found to create CartItem for user: {instance.email}")
#             logger.info(f"Wallet and Shopping Cart created for user: {instance.email}")
#         else:
#             logger.info(f"User updated: {instance.email}")
#     except Exception as e:
#         logger.error(f"An error occurred while creating wallet and cart for user {instance.email}: {e}")

# # Conectar la señal post_save para crear automáticamente una billetera y un carrito cuando se crea un usuario
# post_save.connect(create_wallet_and_cart_for_user, sender=CustomUser)




# logger = logging.getLogger(__name__)
# @receiver(post_save, sender=CustomUser)
# def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
#     """
#     Crea automáticamente una billetera y un carrito de compras para un usuario recién creado y crea un cartitem por carrito.
#     """
#     try:
#         if created:
#             # Crear la billetera
#             Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})

#             cart, created_cart = Cart.objects.get_or_create(user=instance)
#             if created_cart:
#                 # Crear un CartItem predeterminado si es necesario
#                 default_product = Product.objects.first()
#                 if default_product:
#                     CartItem.objects.create(cart=cart, product=default_product, quantity=1, price=0)  # Ajusta esto según tus necesidades
#                 else:
#                     logger.warning(f"No default product found to create CartItem for user: {instance.email}")
#             logger.info(f"Wallet and Shopping Cart created for user: {instance.email}")
#         else:
#             logger.info(f"User updated: {instance.email}")
#     except Exception as e:
#         logger.error(f"An error occurred while creating wallet and cart for user {instance.email}: {e}")

# # Conectar la señal post_save para crear automáticamente una billetera y un carrito cuando se crea un usuario
# post_save.connect(create_wallet_and_cart_for_user, sender=CustomUser)


# @receiver(post_save, sender=CustomUser)
# def create_cart(sender, instance, created, **kwargs):
#     if created:
#         Cart.objects.get_or_create(user=instance)


# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=CustomUser)
# def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
#     """
#     Crea automáticamente una billetera y un carrito de compras para un usuario recién creado y crea un CartItem por carrito.
#     """
#     try:
#         if created:
#             # Crear la billetera
#             Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})

#             # Verificar si el carrito ya existe
#             cart, created_cart = Cart.objects.get_or_create(user=instance)
#             if created_cart:
#                 # Crear un CartItem predeterminado si es necesario
#                 default_product = Product.objects.first()
#                 if default_product:
#                     CartItem.objects.create(cart=cart, product=default_product, quantity=1, price=default_product.price)
#                 else:
#                     logger.warning(f"No default product found to create CartItem for user: {instance.email}")
#             logger.info(f"Wallet and Shopping Cart created for user: {instance.email}")
#         else:
#             logger.info(f"User updated: {instance.email}")
#     except Exception as e:
#         logger.error(f"An error occurred while creating wallet and cart for user {instance.email}: {e}")


# logger = logging.getLogger(__name__)
# @receiver(post_save, sender=CustomUser)
# def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
#     """
#     Crea automáticamente una billetera y un carrito de compras para un usuario recién creado y un CartItem por carrito.
#     """
#     try:
#         if created:
#             # Crear la billetera
#             Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})

#             # Crear el carrito solo si no existe
#             Cart.objects.get_or_create(user=instance)

#             logger.info(f"Wallet and Shopping Cart created for user: {instance.email}")
#         else:
#             logger.info(f"User updated: {instance.email}")
#     except Exception as e:
#         logger.error(f"An error occurred while creating wallet and cart for user {instance.email}: {e}")




logger = logging.getLogger(__name__)
@receiver(post_save, sender=CustomUser)
def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
    """
    Crea automáticamente una billetera y un carrito de compras para un usuario recién creado.
    """
    try:
        if created:
            # Crear la billetera solo si no existe
            wallet, wallet_created = Wallet.objects.get_or_create(
                user=instance, 
                defaults={'currency': 'USD', 'amount': 0}
            )
            
            # Registrar la creación de la billetera
            if wallet_created:
                logger.info(f"Wallet created for user: {instance.email}")
            else:
                logger.info(f"Wallet already exists for user: {instance.email}")
                
            # Crear el carrito solo si no existe
            cart, cart_created = Cart.objects.get_or_create(
                user=instance, 
                defaults={'amount': 0.00}
            )

            # Registrar la creación del carrito
            if cart_created:
                logger.info(f"Shopping Cart created for user: {instance.email}")
            else:
                logger.info(f"Shopping Cart already exists for user: {instance.email}")

    except IntegrityError as e:
        # Capturar errores de integridad, como problemas de unicidad
        logger.error(f"IntegrityError while creating wallet and cart for user {instance.email}: {e}")
    except Exception as e:
        # Capturar cualquier otro error
        logger.error(f"An error occurred while creating wallet and cart for user {instance.email}: {e}")



# @receiver(post_save, sender=CustomUser)
# def create_wallet_and_cart_for_user(sender, instance, created, **kwargs):
#     """
#     Crea automáticamente una billetera y un carrito de compras para un usuario recién creado y un CartItem por carrito.
#     """
#     try:
#         if created:
#             # Crear la billetera
#             Wallet.objects.get_or_create(user=instance, defaults={'currency': 'USD', 'amount': 0})

#             # Crear el carrito solo si no existe
#             # Cart.objects.create(user=instance, amount=0.00)
#             cart, cart_created = Cart.objects.get_or_create(user=instance, amount=0.00)

            
#             if cart_created:
#                 logger.info(f"Wallet and Shopping Cart created for user: {instance.email}")
#             else:
#                 logger.info(f"Shopping Cart already exists for user: {instance.email}")

#     except Exception as e:
#         logger.error(f"An error occurred while creating wallet and cart for user {instance.email}: {e}")
