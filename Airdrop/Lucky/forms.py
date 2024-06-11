from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Product, UserInfo


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
        user = super(CreateAccountForm, self).save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.role = 'customer'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

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
        user = super(CreateManagerForm, self).save(commit=False)
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
