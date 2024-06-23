import logging
from decimal import Decimal


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils.dateformat import DateFormat
from datetime import date
from .forms import CreateAccountForm, ProductForm, UserInfoForm, CustomAuthenticationForm, CreateAdminForm, CreateManagerForm, DiscountCodeForm, ValidateCodeForm, TransferFundsForm  
from .models import Product, UserInfo, CustomUser, DiscountCode, Wallet, Transfer, TransactionsWallet, Store, Cart, CartItem
from django.conf import settings
import stripe
from django.db import transaction


stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def drop(request):
    return render(request, 'drop.html')

@login_required
def header(request):
    return render(request, 'header.html')

@login_required
def some_view(request):
    user_wallet = Wallet.objects.get(user=request.user)
    saldo = user_wallet.amount
    return render(request, 'some_template.html', {'saldo': saldo})

@login_required
def header_view(request):
    if request.user.is_authenticated:
        wallet = Wallet.objects.get(user=request.user)
        saldo = wallet.amount
    else:
        saldo = 0  # o cualquier otro valor por defecto

    context = {
        'saldo': saldo,
        'user': request.user
    }
    return render(request, 'header.html', context)



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


def logout_view(request):
    logout(request)
    return redirect('index.html')  # Redirige a la página de inicio después de cerrar sesión





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


def create_wallet_for_user(email):
    try:
        user = CustomUser.objects.get(email=email)
        # Ajusta según tus necesidades
        wallet = Wallet.objects.create(user=user, currency=1, amount=0)  
        wallet.save()
        print(f"Billetera creada para {user.email}")
    except CustomUser.DoesNotExist:
        print(f"No se encontró ningún usuario con el correo electrónico {email}")

def create_cart_for_user(email):
    try:
        user = CustomUser.objects.get(email=email)
        # Ajusta según tus necesidades
        cart = Cart.objects.create(user=user)  
        cart.save()
        print(f"Carrito creado para {user.email}")
    except CustomUser.DoesNotExist:
        print(f"No se encontró ningún usuario con el correo electrónico {email}")

# Uso de la función
create_wallet_for_user('correo@example.com')




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
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        if created:
            cart.save()  # Guarda el carrito si fue creado
            messages.success(request, 'Your cart was created successfully.')
        cart_items = cart.items.all()
        total_price = sum(item.get_total_price() for item in cart_items)
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'cart.html', context)
    except Exception as e:
        messages.error(request, f'An error occurred while creating your cart: {e}')
        return redirect('shop')  # Redirige a la tienda en caso de error

@login_required
def cart_view(request):
    # Lógica para manejar el carrito
    return render(request, 'cart.html')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from your cart.')
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = request.POST.get('quantity')
    if quantity:
        cart_item.quantity = int(quantity)
        cart_item.save()
    messages.success(request, 'Cart updated.')
    return redirect('cart')




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
def codes(request):
    if request.method == 'POST':
        code = request.POST.get('discount_code')
        try:
            discount_code = DiscountCode.objects.get(code=code)
            if discount_code.is_valid():
                discount_code.used_count += 1
                discount_code.save()
                messages.success(request, f'Código válido! Descuento: {discount_code.discount_percentage}%')
            else:
                messages.error(request, 'Código no válido o expirado.')
        except DiscountCode.DoesNotExist:
            messages.error(request, 'Código no encontrado.')
        return redirect('codes')  # Redirige a la misma página después de procesar el formulario
    return render(request, 'codes.html')

@login_required
def create_discount_code(request):
    if request.method == 'POST':
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Código de descuento creado exitosamente.')
            return redirect('create_discount_code')  # Asegúrate de que 'create_discount_code' sea el nombre correcto del path
    else:
        form = DiscountCodeForm()
    return render(request, 'create_discount_code.html', {'form': form})


@login_required
def manage_discounts(request):
    if request.method == 'POST':
        form = DiscountCodeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Código de descuento creado exitosamente.')
                return redirect('manage_discounts')
            except Exception as e:
                messages.error(request, 'Error al crear el código de descuento. Por favor revise los datos ingresados.')
        else:
            messages.error(request, 'Error al crear el código de descuento. Por favor revise los datos ingresados.')
    else:
        form = DiscountCodeForm()

    discount_codes = DiscountCode.objects.all()
    return render(request, 'manage_discounts.html', {'form': form, 'discount_codes': discount_codes})



@login_required
def validate_code(request):
    if request.method == 'POST':
        form = ValidateCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                discount_code = DiscountCode.objects.get(code=code)
                if discount_code.is_valid():
                    messages.success(request, 'Código de descuento válido.')
                else:
                    messages.error(request, 'Código de descuento inválido o expirado.')
            except DiscountCode.DoesNotExist:
                messages.error(request, 'Código de descuento no encontrado.')
        else:
            messages.error(request, 'Formulario de código de descuento no es válido.')
    else:
        form = ValidateCodeForm()
    return render(request, 'validate_code.html', {'form': form})


# @login_required
# def validate_discount_code(request):
#     if request.method == 'POST':
#         code = request.POST.get('discount_code')
#         try:
#             discount_code = DiscountCode.objects.get(code=code)
#             if discount_code.is_valid():
#                 discount_code.used_count += 1
#                 discount_code.save()
#                 messages.success(request, f'Código válido! Descuento: {discount_code.discount_percentage}%')
#             else:
#                 messages.error(request, 'Código no válido o expirado.')
#         except DiscountCode.DoesNotExist:
#             messages.error(request, 'Código no encontrado.')
#         return redirect('codes')  # Redirige a la misma página después de procesar el formulario
#     return render(request, 'codes.html')


@login_required
def wallet(request):
    user = request.user
    try:
        # Intenta obtener la Wallet del usuario actual
        wallet = Wallet.objects.get(user=user)
        saldo_actual = wallet.amount
    except Wallet.DoesNotExist:
        saldo_actual = 0
        wallet = None

    context = {
        'user': user,
        'wallet': wallet,
        'saldo_actual': saldo_actual,
    }
    return render(request, 'wallet.html', context)




@login_required
def transactions(request):
    return render(request, 'transactions.html')

@login_required
def record(request):
    return render(request, 'record.html')



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


def assign_store(request, user_id, store_id):
    user = get_object_or_404(CustomUser, id=user_id)
    store = get_object_or_404(Store, id=store_id)

    # Asignar la tienda al usuario
    user.stores.add(store)

    return HttpResponse(f'Store {store.name} assigned to user {user.email}')




@login_required
def paypal_form(request):
    return render(request, 'paypal_form.html')

@login_required
def credit_form(request):
    return render(request, 'credit_form.html')

@login_required
def bank_form(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        bank = request.POST.get('bank')
        return HttpResponseRedirect(reverse('transfer_form') + f'?amount={amount}&bank={bank}')
    return render(request, 'bank_form.html')


@login_required
def local_form(request):
    return render(request, 'local_form.html')

@login_required
def transfer(request):
    return render(request, 'transfer.html')



# Este odigo lo comento por si daño en la implementación de los cambios el nuevo

# @login_required
# def transfer_form(request):
#     user = request.user
#     wallet, created = Wallet.objects.get_or_create(user=user)  # Obtener o crear la billetera del usuario
#     bank = request.GET.get('bank', 'Nequi')
#     amount = request.GET.get('amount', '50.000')
#     saldo = wallet.amount  # Obtiene el saldo actual de la billetera
#     context = {
#         'empresa_nombre': 'LuckyCart S.A.',
#         'nit': '900123456-7',
#         'fecha_actual': DateFormat(date.today()).format('Y-m-d'),
#         'estado': 'Completado',
#         'referencia_de_pedido': '199dan-01arbo-06tan-2024med-05col',
#         'referencia_de_transacion': '19920106',
#         'numero_de_transaccion_CUS': '6060928',
#         'banco': bank,
#         'valor': amount,
#         'saldo_actual': saldo,
#         'IP_de_origen': '128.255.255.24'
#     }
#     return render(request, 'transfer_form.html', context)


@login_required
def transfer_form(request):
    if request.method == 'GET':
        form = TransferFundsForm()
        context = {
            'form': form,
            'company_name': 'LuckyCart S.A.',
            'tax_id': '900123456-7',
            'current_date': '2024-06-21',
            'state': 'Completed',
            'order_reference': '199dan-01arbo-06tan-2024med-05col',
            'transaction_reference': '19920106',
            'transaction_number_CUS': '6060928',
            'bank': None,
            'value': None,
            'current_balance': Decimal('0.00'),
            'origin_ip': '127.0.0.1',
            'amount': Decimal('0.00'),
        }
        return render(request, 'transfer_form.html', context)
    elif request.method == 'POST':
        form = TransferFundsForm(request.POST)
        if form.is_valid():
            try:
                amount = form.cleaned_data['amount']
                # Aquí podrías utilizar request.user para obtener el usuario y realizar validaciones adicionales antes de procesar la transacción
                # Ejemplo:
                # user = request.user
                # wallet = Wallet.objects.get(user=user)
                # saldo_actual = wallet.amount
                # Luego procedes con el procesamiento de la transacción similar al ejemplo anterior
            except Exception as e:
                messages.error(request, f'Error processing transaction: {str(e)}')
                return redirect('transfer_form')
        else:
            messages.error(request, 'Invalid form data. Please check the entered data.')
            return render(request, 'transfer_form.html', {'form': form})

    return render(request, 'transfer_form.html')


# @login_required
# def transfer_form_accion(request):
#     user = request.user
#     try:
#         wallet = Wallet.objects.get(user=user)
#         saldo_actual = wallet.amount
#     except Wallet.DoesNotExist:
#         saldo_actual = 0
#         wallet = None

#     if request.method == 'POST':
#         form = TransferFundsForm(request.POST)
#         if form.is_valid():
#             try:
#                 amount = form.cleaned_data['amount']

#                 if amount <= 0:
#                     raise ValueError("El monto debe ser mayor que cero.")

#                 if wallet and saldo_actual >= amount:
#                     with transaction.atomic():
#                         # Create Transfer instance
#                         transferencia = form.save(commit=False)
#                         transferencia.user = user
#                         transferencia.save()

#                         # Update wallet balance
#                         wallet.amount -= amount
#                         wallet.save()

#                     messages.success(request, 'Transferencia realizada exitosamente.')
#                     return redirect('home')
#                 else:
#                     messages.error(request, 'Saldo insuficiente.')
#             except Exception as e:
#                 messages.error(request, f'Error al procesar la transacción: {str(e)}')
#         else:
#             messages.error(request, 'Formulario no válido. Por favor revise los datos ingresados.')
#     else:
#         form = TransferFundsForm()

#     return render(request, 'transfer_form.html', {'form': form, 'saldo_actual': saldo_actual})


logger = logging.getLogger(__name__)

@login_required
@transaction.atomic
def procesar_transaccion(request):
    logger.info('Entering procesar_transaccion')

    if request.method == 'POST':
        user = request.user
        logger.info('Request method is POST')
        logger.info(f'Authenticated user: {user.email}')

        try:
            amount = request.POST.get('amount')
            if not amount:
                raise ValueError("The 'amount' field is empty")

            amount = Decimal(amount)
            logger.info(f'Amount received: {amount}')

            with transaction.atomic():
                wallet, created = Wallet.objects.get_or_create(user=user)
                logger.info(f'Wallet created: {created}')

                wallet.amount += amount
                wallet.save()

                transaction_form = TransferFundsForm(request.POST)
                if transaction_form.is_valid():
                    transaction_instance = transaction_form.save(commit=False)
                    transaction_instance.user = user
                    transaction_instance.wallet = wallet
                    transaction_instance.address_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
                    transaction_instance = transaction_form.save(commit=False)
                    transaction_instance.user = user  # Asignación del usuario obtenido de request.user

                    messages.success(request, f'Transaction successful. ${amount:.2f} added to your balance.')
                    logger.info(f'Transaction successful. ${amount:.2f} added to {user.email}\'s wallet')

                    return redirect('wallet')
                else:
                    raise ValueError("Invalid transaction form")

        except Exception as e:
            messages.error(request, f'Error processing transaction: {str(e)}')
            logger.error(f'Transaction error: {str(e)}')

            return redirect('transfer_form')
    else:
        logger.info(f'Request method is not POST, it is {request.method}')
        messages.error(request, 'Incorrect request method for processing transaction.')

        return redirect('transfer_form')



# @login_required
# def transfer_form(request):
#     amount = request.GET.get('amount')
#     bankName = request.GET.get('bankName')
#     accountNumber = request.GET.get('accountNumber')
#     # Agrega la lógica de tu vista aquí
#     return render(request, 'transfer_form.html', {
#         'amount': amount,
#         'bankName': bankName,
#         'accountNumber': accountNumber,
#     })

# @login_required
# def transfer_funds(request):
#     try:
#         user_wallet = Wallet.objects.get(id_user=request.user.id)
#     except Wallet.DoesNotExist:
#         messages.error(request, "Wallet not found for the user.")
#         print("Redirigiendo a la vista 'transfer' porque no se encontró la wallet.")
#         # return redirect('transfer')  # Asegúrate de que esta vista no redirija de nuevo a 'transfer_funds'

#     if request.method == 'POST':
#         form = TransferFundsForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             user_wallet.amount += amount
#             user_wallet.save()
#             messages.success(request, 'Funds transferred successfully!')
#             return redirect('home')  # Asegúrate de que 'home' no redirija de nuevo a 'transfer_funds'
#     else:
#         form = TransferFundsForm()

#     return render(request, 'transfer_funds.html', {'form': form, 'saldo': user_wallet.amount})



def process_payment(request):
    if request.method == 'POST':
        amount = int(request.POST['amount']) * 100
        currency = 'usd'
        success_url = request.build_absolute_uri(reverse('payment_success'))
        cancel_url = request.build_absolute_uri(reverse('payment_cancel'))
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Example Product',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return JsonResponse({'id': session.id})
    return render(request, 'process_payment.html')

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_cancel(request):
    return render(request, 'payment_cancel.html')

@login_required
def initiate_transfer(request):
    saldo = 0  # Inicializar saldo en 0 para evitar problemas si el usuario no tiene una billetera
    if request.method == 'POST':
        form = transfer_form(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Obtener los datos del formulario
                    empresa = form.cleaned_data['empresa']
                    nit = form.cleaned_data['nit']
                    fecha = form.cleaned_data['fecha']
                    estado = form.cleaned_data['estado']
                    refPedido = form.cleaned_data['refPedido']
                    refTransaccion = form.cleaned_data['refTransaccion']
                    numTransaccion = form.cleaned_data['numTransaccion']
                    bank = form.cleaned_data['bank']
                    amount = form.cleaned_data['amount']
                    ipOrigen = form.cleaned_data['ipOrigen']

                    # Crear una nueva transferencia
                    transferencia = Transfer(
                        empresa=empresa,
                        nit=nit,
                        fecha=fecha,
                        estado=estado,
                        refPedido=refPedido,
                        refTransaccion=refTransaccion,
                        numTransaccion=numTransaccion,
                        bank=bank,
                        amount=amount,
                        ipOrigen=ipOrigen,
                        user=request.user
                    )
                    transferencia.save()

                    # Actualizar el saldo de la billetera del usuario
                    wallet = Wallet.objects.get(user=request.user)
                    if wallet.amount >= amount:
                        wallet.amount -= amount
                        wallet.save()
                    else:
                        raise ValueError("Saldo insuficiente")


                    messages.success(request, 'Transacción realizada exitosamente.')
                    return redirect('home')
            except Exception as e:
                messages.error(request, f'Error al realizar la transacción: {str(e)}')
        else:
            messages.error(request, 'Error en el formulario de transferencia. Por favor revise los datos ingresados.')
    else:
        # Prellenar el formulario con datos del usuario y la fecha actual
        initial_data = {
            'empresa': 'Nombre de la Empresa',
            'nit': '1234567890',
            'fecha': date.today(),
            'refPedido': 'REF123456',
            'refTransaccion': 'TRANS123456',
            'numTransaccion': 'CUS123456',
            'bank': 'Nombre del Banco',
            'amount': 100,  # Valor por defecto, cambiar según sea necesario
            'ipOrigen': request.META.get('REMOTE_ADDR', '127.0.0.1')
        }
        form = TransferFundsForm(initial=initial_data)

        # Obtener el saldo de la billetera del usuario
        try:
            wallet = Wallet.objects.get(user=request.user)
            saldo = wallet.amount
        except Wallet.DoesNotExist:
            saldo = 0  # Si el usuario no tiene una billetera, establecer saldo en 0
    return render(request, 'transfer_form.html', {'form': form})

@login_required
def update_transfer(request):
    if request.method == 'POST':
        refTransaccion = request.POST.get('refTransaccion')
        amount = request.POST.get('amount')

        if refTransaccion and amount:
            try:
                with transaction.atomic():
                    # Obtener la transferencia por su referencia
                    transferencia = get_object_or_404(Transfer, refTransaccion=refTransaccion)

                    # Calcular la diferencia en el monto
                    diferencia = amount - transferencia.amount

                    # Actualizar el monto de la transferencia
                    transferencia.amount = amount
                    transferencia.save()

                    # Actualizar el saldo de la billetera del usuario
                    wallet = Wallet.objects.get(user=request.user)
                    if wallet.amount >= diferencia:
                        wallet.amount -= diferencia
                        wallet.save()
                    else:
                        raise ValueError("Saldo insuficiente para la actualización")

                    messages.success(request, 'Transferencia actualizada exitosamente.')
                    return redirect('home')
            except Exception as e:
                messages.error(request, f'Error al actualizar la transferencia: {str(e)}')
        else:
            messages.error(request, 'Debe proporcionar una referencia de transacción y un monto.')
    else:
        messages.error(request, 'Solicitud inválida.')

    return redirect('home')