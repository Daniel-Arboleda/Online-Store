from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import open_account, create_account, product_create_view
# from .views import open_account, create_account, products, update_user_info
# from .views import open_account, create_account, products, user_info
from .views import open_account, products, user_info


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('drop/', views.drop, name='drop'),
    path('login/', views.login_form, name='login_form'),
    path('open/', views.open_account, name='open_account'),
    path('home/', views.home, name='home'),
    path('home_orm/', views.home_orm, name='home_orm'),
    path('user/', views.user, name='user'),
    path('user_info/', views.user_info, name='user_info'),
    path('cart/', views.cart, name='cart'),
    path('products/', views.products, name='products'),
    path('shop/', views.shop, name='shop'),
    path('delivery/', views.delivery, name='delivery'),
    path('wallet/', views.wallet, name='wallet'),
    path('transactions/', views.transactions, name='transactions'),
    path('record/', views.record, name='record'),
    path('codes/', views.codes, name='codes'),
    path('transfer/', views.transfer, name='transfer'),
    path('transfer_form/', views.transfer_form, name='transfer_form'),
    path('paypal_form/', views.paypal_form, name='paypal_form'),
    path('credit_form/', views.credit_form, name='credit_form'),
    path('bank_form/', views.bank_form, name='bank_form'),
    path('local_form/', views.local_form, name='local_form'),
    

    # Validación de los datos de formulario crear cuenta o inicio de sesion cuando es externa
    # path('create-account/', views.create_account, name='create_account'),
    # Ruta para la creación de los productos mediante el formulario
    # path('create_product/', product_create_view, name='create_product'),
    # path('products/', product_create_view, name='products'),
    # Ruta para la creación del render del la vista para las tablas de los productos mediante el formulario... Este método es para visualizar la lista en una página diferente a la del formulario
    # path('products/list/', views.product_list, name='product_list'),

    # Ruta extena para renderizar el formulario de datos del usuario 
    # path('update-info/', update_user_info, name='update_user_info'),


    # Método para la url del botón eleiminar producto de la tabla de stock
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    # Verifica si el parametro existe en la DB tabla Products
    path('check_product_existence/', views.check_product_existence, name='check_product_existence'),
    # Compara las variables para conocer si pertenecen al mismo producto en la DB
    path('check_product_fields/', views.check_product_fields, name='check_product_fields'),



    # Método para renderizar el autocargado del formulario
    path('get_product_details/', views.get_product_details, name='get_product_details'),








    # Pasarelas de pago Stripe
    path('charge/', views.charge, name='charge'),
    # Pasarelas de pago Paypal
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/execute/', views.payment_execute, name='payment_execute'),
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
    


    # path('product_list_view/', views.product_list_view, name='product_list'),
    # path('create-product/', product_create_view, name='create_product'),
    # # Otras rutas...


    # path('accounts/', include('django.contrib.auth.urls')),


] 

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
