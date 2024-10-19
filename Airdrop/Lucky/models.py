# models.py


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission, User
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import Product  # Si permito esta línea de código genra una importació´n circular dentro del mismo documento models.py por tanto el documento llama lafunción y la fución al docuemnto y esto genrra que el servidor colapse.



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # Guardar el usuario primero
        user.save(using=self._db)
        # Crear la billetera asociada al usuario
        # Wallet.objects.create(user=user, user_email=email)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != 'superuser':
            raise ValueError('Superuser must have role="superuser"')
        return self.create_user(email, password, **extra_fields)

    def create_admin_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != 'superuser':
            raise ValueError('Superuser must have role="superuser"')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('superuser', 'Superuser'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
    ]

    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_number = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='customer')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Auth'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email



# User = get_user_model()


class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wallet')
    # user_email = models.EmailField(unique=True)
    currency = models.CharField(max_length=3, default='USD')
    last_update_date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Wallet for {self.user.email} - ${self.amount}"

    class Meta:
        db_table = 'Wallet'


class TransactionsWallet(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True, blank=True)
    # user_id = models.IntegerField(blank=True)
    # wallet_id = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    date_hour = models.IntegerField(blank=True)
    type = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    address_ip = models.TextField(blank=True)
    state = models.TextField(blank=True)
    transfer_method = models.TextField(null=True, blank=True)
    bank = models.TextField(blank=True)
    company_name = models.TextField(blank=True)
    tax_id = models.TextField(blank=True)
    order_reference = models.TextField(blank=True)
    transaction_reference = models.TextField(blank=True)
    transaction_number_CUS = models.TextField(blank=True)

    def __str__(self):
        return f"Transaction {self.order_reference} by {self.user.email}"

    class Meta:
        db_table = 'TransactionsWallet'


# OneToOneField establece una relación de uno a uno entre dos modelos. Esto significa que cada instancia de UserInfo está vinculada a una única instancia de User y viceversa. Es similar a ForeignKey, pero asegura que no haya múltiples registros en UserInfo asociados con un solo User.
class UserInfo(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('PA', 'Pasaporte'),
        ('TI', 'Registro Civil'),
        ('RC', 'Tarjeta de identidad'),
        ('DNI', 'Documento Nacional de Identificación'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='userinfo')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    type_document = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES, blank=True)  # Ajustar max_length
    document = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    address = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'Users'  # Nombre de la tabla en la base de datos
        verbose_name = 'User Info'
        verbose_name_plural = 'User Infos'

    def __str__(self):
        return f"{self.user.email} - {self.type_document}: {self.document}"







class Product(models.Model):
    DISPONIBILITY_CHOICES = [
        ('available', 'Disponible'),
        ('out_of_stock', 'Agotado'),
        ('coming_soon', 'Próximamente Disponible'),
        ('reserved', 'Reservado'),
        ('discontinued', 'Descontinuado'),
        ('in_transit', 'En Tránsito'),
        ('pending', 'Pendiente'),
        ('returned', 'Devuelto'),
        ('under_repair', 'En Reparación'),
        ('not_for_sale', 'No Disponible para Venta'),
        ('being_retired', 'En Proceso de Retiro'),
        ('in_negotiation', 'En Negociación'),
        ('sold_out', 'Agotado'),
        ('available_now', 'Disponible Ahora'),
        ('temporarily_unavailable', 'Temporalmente No Disponible'),
        ('pre_order', 'Preorden'),
        ('backorder', 'Pedido Pendiente'),
        ('special_order', 'Pedido Especial'),
        ('limited_stock', 'Stock Limitado'),
        ('awaiting_restock', 'Esperando Reabastecimiento'),
        ('to_be_demolished', 'Para Ser Demolido'),
    ]
    
    STATE_CHOICES = [
        ('NEW', 'Nuevo'),
        ('USED', 'Usado'),
        ('REFURBISHED', 'Reacondicionado'),
        ('DAMAGED', 'Dañado'),
        ('OPEN_BOX', 'Caja Abierta'),
        ('FOR_PARTS', 'Para Piezas'),
        ('for_sale', 'En Venta'),
        ('for_rent', 'En Renta'),
        ('sale_in_progress', 'En Proceso de Venta'),
        ('rented', 'Rentada'),
        ('under_contract', 'Bajo Contrato'),
        ('available_soon', 'Disponible Pronto'),
        ('under_renovation', 'En Renovación'),
        ('under_maintenance', 'En Mantenimiento'),
        ('under_construction', 'En Construcción'),
        ('new_listing', 'Nuevo Listado'),
        ('off_market', 'Fuera del Mercado'),
        ('foreclosed', 'Embargada'),
        ('auction', 'Subasta'),
        ('pending_inspection', 'Pendiente de Inspección'),
        ('contingent', 'Contingente'),
        ('move_in_ready', 'Listo para Mudanza'),
        ('fixer_upper', 'Para Renovar'),
        ('historical', 'Histórico'),
        ('luxury', 'Lujo'),
        ('eco_friendly', 'Ecológico'),
    ]
    
    CATEGORY_CHOICES = [
        ('housing', 'Vivienda'),
        ('vehicles', 'Vehículos'),
        ('technology', 'Tecnología'),
        ('fashion', 'Moda'),
        ('accessories', 'Accesorios'),
    ]
    
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=13, decimal_places=2)
    stock = models.IntegerField()
    categories = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True, default='technology')
    brand = models.CharField(max_length=100)
    disponibility = models.CharField(max_length=50, choices=DISPONIBILITY_CHOICES, blank=True, null=True, default='coming_soon')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, blank=True, null=True, default='NEW')
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    class Meta:
        db_table = 'Products'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name

    
    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False


    



class Store(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_stores')
    # Otros campos necesarios para la tienda

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        db_table = 'Cart'
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return f"Cart of {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    # cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='item')
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)



    class Meta:
        db_table = 'CartItem'
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')


    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.email}'s cart"

    def get_total_price(self):
        return self.product.price * self.quantity

    # def save(self, *args, **kwargs):
    #     self.amount = self.get_total_price()
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.product.reduce_stock(self.quantity):
            self.amount = self.get_total_price()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Not enough stock available")





class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_uses = models.IntegerField()
    used_count = models.IntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to and self.used_count < self.max_uses

    class Meta:
        db_table = 'DiscountCode'


    
class Transfer(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of {self.amount} to {self.wallet.user.username}'s Wallet"