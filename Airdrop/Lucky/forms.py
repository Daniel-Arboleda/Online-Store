
# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.core.exceptions import ValidationError
# from .models import CustomUser

from django import forms
from .models import CustomUser, Product, UserInfo
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
    def save(self, commit=True):
        user = super(CreateAccountForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'price', 'stock', 'categories', 'brand', 'state', 'image']
        widgets = {
            'state': forms.Select(choices=Product.STATE_CHOICES),
        }

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['first_name', 'last_name', 'type_document', 'document', 'phone', 'address']
