from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Product, UserInfo, CustomUser

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.role = 'customer'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
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

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'type_document', 'document', 'phone', 'address']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'price', 'stock', 'categories', 'brand', 'state', 'disponibility', 'image']
        widgets = {
            'categories': forms.Select(choices=Product.CATEGORY_CHOICES),
            'state': forms.Select(choices=Product.STATE_CHOICES),
            'disponibility': forms.Select(choices=Product.DISPONIBILITY_CHOICES),
        }
