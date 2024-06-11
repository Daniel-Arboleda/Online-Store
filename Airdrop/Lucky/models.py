from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')  # Establecer el rol como 'superuser'

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
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='customer')
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Auth'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email



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

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userinfo')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    type_document = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES, blank=True)  # Ajustar max_length
    document = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

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
    image = models.ImageField(upload_to="images/")

    class Meta:
        db_table = 'Products'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name