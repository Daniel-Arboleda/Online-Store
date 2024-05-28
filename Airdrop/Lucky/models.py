from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
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
        db_table = 'Users'  # Asegúrate de que el nombre de la tabla es correcto
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email





class Product(models.Model):
    STATE_CHOICES = [
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
    ]
    CATEGORY_CHOICES = [
    ('housing', 'Vivienda'),
    ('vehicles', 'Vehículos'),
    ('technology', 'Tecnología'),
    ('fashion', 'Moda'),
    ('accessories', 'Accesorios'),
    ]
    # id = models.AutoField()
    code= models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=13, decimal_places=2)
    stock = models.IntegerField() 
    categories = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technology') 
    brand = models.CharField(max_length=100)  
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='coming_soon') 
    image = models.ImageField(upload_to="images/")

    class Meta:
        db_table = 'Products'  # Asegúrate de que el nombre de la tabla es correcto
        verbose_name = _('product')
        verbose_name_plural = _('product')

    def __str__(self):
        return self.name
