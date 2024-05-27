from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from paypalrestsdk import Payment, configure
from django.conf import settings
from datetime import date
import stripe


def index(request):
    return render(request, 'index.html')
def drop(request):
    return render(request, 'drop.html')
def login_form(request):
    return render(request, 'login_form.html')
def open_account(request):
    return render(request, 'open_account.html')
def home(request):
    return render(request, 'home.html')
def home_orm(request):
    return render(request, 'home_orm.html')
def user(request):
    return render(request, 'user.html')
def user_info(request):
    return render(request, 'user_info.html')
def cart(request):
    return render(request, 'cart.html')
def products(request):
    return render(request, 'products.html')
def shop(request):
    return render(request, 'shop.html')
def delivery(request):
    return render(request, 'delivery.html')
def wallet(request):
    return render(request, 'wallet.html')
def transactions(request):
    return render(request, 'transactions.html')
def record(request):
    return render(request, 'record.html')
def codes(request):
    return render(request, 'codes.html')
def transfer(request):
    return render(request, 'transfer.html')
def transfer_form(request):
    return render(request, 'transfer_form.html')
def paypal_form(request):
    return render(request, 'paypal_form.html')
def credit_form(request):
    return render(request, 'credit_form.html')
def bank_form(request):
    return render(request, 'bank_form.html')
def local_form(request):
    return render(request, 'local_form.html')

# def product_list_view(request):
#     products = Product.objects.all()
#     return render(request, 'product_list.html', {'products': products})


from django.shortcuts import render, redirect
from .forms import CreateAccountForm, ProductForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
import logging
from .models import Product


# def open_account(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         hashed_password = make_password(password)

#         if not User.objects.filter(email=email).exists():
#             user = User(email=email, password=hashed_password)
#             user.save()
#             return redirect('success')  # Redirige a una página de éxito
#         else:
#             return render(request, 'open_account.html', {'error': 'Email already in use'})
#     return render(request, 'open_account.html')




logger = logging.getLogger(__name__)
# Configuración para definir el metodo que manejara las solicitudes de POST en el formulario de crear cuenta
def create_account(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)  # Inicia sesión con el usuario creado
                messages.success(request, 'Cuenta creada exitosamente.')
                logger.debug("Cuenta creada con éxito para el usuario: %s", user.email)
                return redirect('home')  # Redirige a la página de inicio
            except Exception as e:
                logger.error("Error al crear la cuenta: %s", e)
                messages.error(request, 'Error al crear la cuenta. Por favor revise los datos ingresados.')
                # Intento crear un usuario
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)  # Inicia sesión con el usuario creado
                messages.success(request, 'Cuenta creada exitosamente.')
                logger.debug("Cuenta creada con éxito para el usuario: %s", username)
                return redirect('home')  # Redirige a la página de inicio
            except Exception as e:
                logger.error("Error al crear la cuenta para el usuario %s: %s", username, e)
                messages.error(request, 'Error al crear la cuenta. Por favor revise los datos ingresados.')
                # Es opcional re-lanzar la excepción, depende de cómo quieras manejarla
        else:
            logger.warning("Formulario de creación de cuenta no es válido: %s", form.errors)
            messages.error(request, 'Error al crear la cuenta. Por favor revise los datos ingresados.')
    else:
        form = CreateAccountForm()
    return render(request, 'open_account.html', {'form': form})



logger = logging.getLogger(__name__)
def product_create_view(request):
    if request.method == 'POST':
        logger.debug("POST request received.")
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.debug("Form is valid.")
            # logger.info("Producto guardado exitosamente")
            # print("Producto guardado exitosamente")
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('products')  # Redirigir a una vista de lista de productos o alguna otra vista de éxito
        else:
            logger.warning("Formulario no válido: %s", form.errors)
            messages.error(request, 'Error al crear el producto. Por favor revise los datos ingresados.')
            # print("Formulario no válido")
            # print(form.errors)
    else:
        logger.debug("GET request received.")
        form = ProductForm()
    return render(request, 'products.html', {'form': form})





# Autorellenar el formulario de transfer_form

def transfer_form(request):
    context = {
        'empresa_nombre': 'LuckyCart S.A.',
        'nit': '900123456-7',
        'fecha_actual': date.today().isoformat(),  # Formato AAAA-MM-DD
        'estado' : 'Completado',
        'referencia_de_pedido' : '199dan-01arbo-06tan-2024med-05col',
        'referencia_de_transacion' : '19920106',
        'numero_de_transaccion_CUS' : '6060928',
        'banco' : 'nequi',
        'valor' : '50.000',
        'moneda' : 'cop',
        'IP_de_origen' : '128.255.255.24'

    }
    return render(request, 'transfer_form.html', context)





# # Cookies con seguridad para manejo de respuestas de saldo
# def mi_vista(request):
#     # Aquí iría la lógica de tu vista
#     response = HttpResponse("Mensaje")
#     response.set_cookie('saldo', 'valor_del_saldo', httponly=True, secure=True)
#     return response




# def process_transfer(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         # Aquí iría la lógica para procesar el pago y actualizar el saldo
#         # Por ejemplo, actualizar el saldo del usuario en la base de datos
#         new_balance = update_user_balance(request.user, amount)
#         return JsonResponse({'success': True, 'new_balance': new_balance})
#     return JsonResponse({'success': False})



# @login_required
# def get_saldo(request):
#     # Asume que tienes un método para obtener el saldo del usuario
#     saldo = request.user.get_saldo()
#     return JsonResponse({'saldo': saldo})

    # Configuraci´on de las pasarelas de pago
# Configurar la clave secreta de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
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
            return render(request, 'payments/charge_fail.html', {'error': str(e)})

    return render(request, 'payments/charge_form.html')

# Configuración de paypal
configure({
  "mode": settings.PAYPAL_MODE,  # sandbox or live
  "client_id": settings.PAYPAL_CLIENT_ID,
  "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def payment_process(request):
    if request.method == 'POST':
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": "10.00",
                    "currency": "USD"
                },
                "description": "Descripción del pago."
            }],
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment/execute/'),
                "cancel_url": request.build_absolute_uri('/payment/cancelled/')
            }
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    # Redirigir al usuario al approval_url
                    return redirect(link.href)
        else:
            print(payment.error)
            return render(request, 'payments/payment_error.html')

    return render(request, 'payments/payment_form.html')

def payment_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payments/payment_success.html')
    else:
        return render(request, 'payments/payment_error.html')

def payment_cancelled(request):
    return HttpResponse("Pago cancelado.")

# @login_required
# def transfer_form(request):
#     return render(request, 'transfer_form.html')
    