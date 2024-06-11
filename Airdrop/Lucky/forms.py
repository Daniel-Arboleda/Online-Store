
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


# class CreateBuyerForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super(CreateBuyerForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.is_staff = False  # Asegurar que no sea staff
#         if commit:
#             user.save()
#         return user

def open_admin_account(request):
    if not request.user.is_superuser:
        return HttpResponse('No tienes permiso para acceder a esta página.', status=403)

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Administrador creado exitosamente.')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'Error al crear el Administrador. Por favor revise los datos ingresados.')
        else:
            messages.error(request, 'Formulario no válido. Por favor revise los datos ingresados.')
    else:
        form = UserCreationForm()
    return render(request, 'open_admin_account.html', {'form': form})



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