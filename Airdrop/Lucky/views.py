from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from datetime import date
from .forms import CreateAccountForm, ProductForm, UserInfoForm, CustomAuthenticationForm, CreateAdminForm, CreateManagerForm
from .models import Product, UserInfo, CustomUser
from django.conf import settings
import stripe
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def drop(request):
    return render(request, 'drop.html')

@login_required
def header(request):
    return render(request, 'header.html')


def login_form(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                print(f"Email '{email}' exists in Auth table: True")
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Correo o contraseña incorrectos.")
            except CustomUser.DoesNotExist:
                print(f"Email '{email}' does not exist in Auth table.")
                messages.error(request, "Correo o contraseña incorrectos.")
        else:
            messages.error(request, "Ambos campos son obligatorios.")
        print("Formulario inválido. Errores:", form.errors)
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login_form.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = EmailAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 form.add_error(None, 'Invalid email or password')
#     else:
#         form = EmailAuthenticationForm()
#     return render(request, 'login_form.html', {'form': form})




# def login_form(request):
#     if request.method == 'POST':
#         print("Formulario enviado")
#         form = CustomAuthenticationForm(request, data=request.POST)
#         print("Datos del formulario:", form.data)
#         if form.is_valid():
#             print("Formulario válido")
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             print("Datos limpios del formulario - Email:", email, "Password:", password)
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 print("Usuario autenticado:", user)
#                 login(request, user)
#                 logger.info(f"User {user.email} logged in successfully.")
#                 return redirect('home')
#             else:
#                 print("Usuario no encontrado")
#                 logger.warning(f"Login attempt failed for email: {email}")
#                 messages.error(request, 'Usuario o contraseña incorrectos.')
#         else:
#             print("Formulario inválido. Errores:", form.errors)
#             logger.warning(f"Invalid login form submitted: {form.errors}")
#             messages.error(request, 'Formulario no válido. Por favor revise los datos ingresados.')
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'login_form.html', {'form': form})


def open_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Cuenta creada exitosamente.')
                logger.debug("Cuenta creada con éxito para el usuario: %s", user.email)
                return redirect('home')
            except Exception as e:
                logger.error("Error al crear la cuenta: %s", e)
                messages.error(request, 'Error al crear la cuenta. Por favor revise los datos ingresados.')
        else:
            logger.warning("Formulario de creación de cuenta no es válido: %s", form.errors)
            messages.error(request, 'Error al crear la cuenta. Por favor revise los datos ingresados.')
    else:
        form = CreateAccountForm()
    return render(request, 'open_account.html', {'form': form})


@login_required
@staff_member_required
def open_admin_account(request):
    if not request.user.is_superuser:
        return HttpResponse('No tienes permiso para acceder a esta página.', status=403)

    max_superusers = 5
    current_superusers = CustomUser.objects.filter(is_superuser=True).count()

    if current_superusers >= max_superusers:
        messages.error(request, 'No se puede crear más de %d superusuarios.' % max_superusers)
        return redirect('home')

    if request.method == 'POST':
        form = CreateAdminForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Administrador creado exitosamente.')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'Error al crear el Administrador. Por favor revise los datos ingresados.')
                logger.error("Error al crear el Administrador: %s", e)
        else:
            messages.error(request, 'Formulario no válido. Por favor revise los datos ingresados.')
    else:
        form = CreateAdminForm()

    return render(request, 'open_admin_account.html', {'form': form})



@login_required
def open_manager_account(request):
    if not request.user.is_superuser:
        return HttpResponse('No tienes permiso para acceder a esta página.', status=403)

    if request.method == 'POST':
        form = CreateManagerForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Manager creado exitosamente.')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'Error al crear el Manager. Por favor revise los datos ingresados.')
        else:
            messages.error(request, 'Formulario no válido. Por favor revise los datos ingresados.')
    else:
        form = CreateManagerForm()
    return render(request, 'open_manager_account.html', {'form': form})


@login_required
def home(request):
    current_year = date.today().year
    return render(request, 'home.html', {'current_year': current_year})

@login_required
def home_orm(request):
    return render(request, 'home_orm.html')

@login_required
def user(request):
    return render(request, 'user.html', {'user': request.user})






@login_required
def user_info(request):
    user_instance = get_object_or_404(CustomUser, pk=request.user.pk)
    user_info_instance, created = UserInfo.objects.get_or_create(user=user_instance)

    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=user_info_instance)
        if form.is_valid():
            user_info = form.save(commit=False)
            user_info.user = user_instance  # Aseguramos que user_info esté asociado al usuario correcto
            user_info.save()

            # También actualizamos el objeto CustomUser
            user_instance.first_name = form.cleaned_data['first_name']
            user_instance.last_name = form.cleaned_data['last_name']
            user_instance.save()

            messages.success(request, 'Datos personales actualizados exitosamente.')
            return redirect('user_info')
        else:
            messages.error(request, 'Por favor corrija los errores a continuación.')
    else:
        form = UserInfoForm(instance=user_info_instance)

    return render(request, 'user_info.html', {
        'form': form,
        'user': user_instance,
        'user_info': user_info_instance
    })







@login_required
def cart(request):
    return render(request, 'cart.html')

@login_required
def products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('products')
        else:
            messages.error(request, 'Error al crear el producto. Por favor revise los datos ingresados.')
    else:
        form = ProductForm()
    
    products = Product.objects.all()
    return render(request, 'products.html', {'form': form, 'products': products})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
    return redirect(reverse('products'))

def check_product_existence(request):
    code = request.GET.get('code', None)
    name = request.GET.get('name', None)

    response = {
        'code_exists': Product.objects.filter(code=code).exists() if code else False,
        'name_exists': Product.objects.filter(name=name).exists() if name else False,
    }

    return JsonResponse(response)

def get_product_details(request):
    code = request.GET.get('code')
    name = request.GET.get('name')

    product_by_code = Product.objects.filter(code=code).first() if code else None
    product_by_name = Product.objects.filter(name=name).first() if name else None

    response_data = {
        'code_exists': bool(product_by_code),
        'name_exists': bool(product_by_name),
        'message': '',
        'product': None
    }

    if product_by_code and product_by_name:
        if product_by_code.id == product_by_name.id:
            response_data['message'] = 'Ambos campos son del mismo producto'
            response_data['product'] = {
                'id': product_by_code.id,
                'description': product_by_code.description,
                'price': product_by_code.price,
                'stock': product_by_code.stock,
                'categories': product_by_code.categories,
                'brand': product_by_code.brand,
                'state': product_by_code.state,
                'disponibility': product_by_code.disponibility,
            }
        else:
            response_data['message'] = 'Los campos pertenecen a productos distintos'
    elif product_by_code:
        response_data['message'] = 'El nombre del producto no existe en la DB'
    elif product_by_name:
        response_data['message'] = 'El código del producto no existe en la DB'
    else:
        response_data['message'] = 'Crear nuevo producto'

    return JsonResponse(response_data)

def shop(request):
    categories = Product.CATEGORY_CHOICES
    products_by_category = {category_name: Product.objects.filter(categories=category_code) 
                            for category_code, category_name in categories}
    
    context = {
        'products_by_category': products_by_category,
        'total_products': Product.objects.count(),
    }
    
    return render(request, 'shop.html', context)

@login_required
def delivery(request):
    return render(request, 'delivery.html')

@login_required
def wallet(request):
    return render(request, 'wallet.html')

@login_required
def transactions(request):
    return render(request, 'transactions.html')

@login_required
def record(request):
    return render(request, 'record.html')

@login_required
def codes(request):
    return render(request, 'codes.html')

@login_required
def charge(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')

        try:
            # Crear el cargo en Stripe
            charge = stripe.Charge.create(
                amount=1000,  # $10.00 cobrado
                currency='usd',
                description='Descripción del producto o servicio',
                source=token
            )
            return render(request, 'payments/charge_success.html')
        except stripe.error.StripeError as e:
            logger.error("Stripe error: %s", e)
            return render(request, 'payments/charge_fail.html', {'error': str(e)})

    return render(request, 'payments/charge_form.html')

@login_required
def transfer(request):
    return render(request, 'transfer.html')

@login_required
def transfer_form(request):
    context = {
        'empresa_nombre': 'LuckyCart S.A.',
        'nit': '900123456-7',
        'fecha_actual': date.today().isoformat(),  # Formato AAAA-MM-DD
        'estado': 'Completado',
        'referencia_de_pedido': '199dan-01arbo-06tan-2024med-05col',
        'referencia_de_transacion': '19920106',
        'numero_de_transaccion_CUS': '6060928',
        'banco': 'nequi',
        'valor': '50.000',
        'moneda': 'cop',
        'IP_de_origen': '128.255.255.24'
    }
    return render(request, 'transfer_form.html', context)


@login_required
def paypal_form(request):
    return render(request, 'paypal_form.html')

@login_required
def credit_form(request):
    return render(request, 'credit_form.html')

@login_required
def bank_form(request):
    return render(request, 'bank_form.html')

@login_required
def local_form(request):
    return render(request, 'local_form.html')
