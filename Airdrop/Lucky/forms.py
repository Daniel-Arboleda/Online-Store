from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from .models import Product, UserInfo, CustomUser, UserInfo, DiscountCode, TransactionsWallet, Cart, Wallet

class CreateSuperuserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        user.role = 'superuser'
        if commit:
            user.save()
        return user

class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.role = 'customer'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Cart.objects.create(user=user)
            Wallet.objects.create(user=user, user_email=user.email, currency='USD', amount=0)
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("Correo electrónico"), max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label=_("Contraseña"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    error_messages = {
        'invalid_login': _(
            "Por favor, introduzca un correo electrónico y contraseña correctos. Observe que ambos campos pueden ser sensibles a mayúsculas."
        ),
        'inactive': _("Esta cuenta está inactiva."),
    }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )



class CreateAdminForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'autocomplete': 'username'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = False
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']

        if commit:
            user.save()
        return user

class CreateManagerForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        user.is_superuser = False
        if commit:
            user.save()
        return user




# Esta clase se crea para manejar los campos del formulario user_info.html que es la información personal del susuario dueño de la cuenta.
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'type_document', 'document', 'nationality', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_document': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtenemos el usuario asociado al formulario
        user = self.instance.user
        # Establecemos el valor del campo 'email' con el email del usuario
        self.fields['email'] = forms.EmailField(label='Email', initial=user.email, disabled=True)


    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if UserInfo.objects.filter(phone=phone).exclude(user=self.instance.user).exists():
            raise forms.ValidationError('El número de teléfono ya está en uso por otro usuario.')
        return phone








# Clase que maneja los campos del formulario para el formulario de productcs.html donde se crea los productos neuos o se actualizan
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'price', 'stock', 'categories', 'brand', 'state', 'disponibility', 'image']
        widgets = {
            'categories': forms.Select(choices=Product.CATEGORY_CHOICES),
            'state': forms.Select(choices=Product.STATE_CHOICES),
            'disponibility': forms.Select(choices=Product.DISPONIBILITY_CHOICES),
        }



class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = ['code', 'discount_percentage', 'max_uses', 'valid_from', 'valid_to', 'is_active']

class ValidateCodeForm(forms.Form):
    code = forms.CharField(max_length=50)


# Clase que maneja los campos del formulario de transfer_funds el cual es un fomrulario de los campos de infomación de formulario e transacción para cargar saldo el primero que e configura pero maneja la logica mediante los TANG's de Django para la creación de campos de formularios HTML, por lo que en uso actuak puede no estar en uso, sin embargo puede usarse como variablke conectorea o de consulta ----------- Se debe tener cuidado porque esto puede generar un FONEL y SCRATCH de projecct, lo que seria en programación en funcionamiento una ruta crítica

class TransferFundsForm(forms.ModelForm):
    company_name = forms.CharField(max_length=100, required=False)
    tax_id = forms.CharField(max_length=20, required=False)
    current_date = forms.DateField(required=False)
    state = forms.CharField(max_length=20, required=False)
    order_reference = forms.CharField(max_length=50, required=False)
    transaction_reference = forms.CharField(max_length=50, required=False)
    transaction_number_CUS = forms.CharField(max_length=50, required=False)
    bank = forms.CharField(max_length=50, required=False)
    value = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    current_balance = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    origin_ip = forms.CharField(max_length=15, required=False)
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)

    class Meta:
        model = TransactionsWallet
        fields = [
            'company_name', 'tax_id', 'current_date', 'state', 'order_reference', 
            'transaction_reference', 'transaction_number_CUS', 'bank', 'value', 
            'current_balance', 'origin_ip', 'amount'
        ]