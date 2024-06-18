from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from Lucky import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('drop/', views.drop, name='drop'),

    path('header/', views.header, name='header'),
    path('login/', views.login_form, name='login_form'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Esto redirige a la página principal después del logout
    path('open/', views.open_account, name='open_account'),
    # path('open_buyer_account/', views.open_buyer_account, name='open_buyer_account'),
    path('open_manager_account/', views.open_manager_account, name='open_manager_account'),
    path('open_admin_account/', views.open_admin_account, name='open_admin_account'),

    # path('logout/', LogoutView.as_view(), name='logout'),

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
    path('create_discount_code/', views.create_discount_code, name='create_discount_code'),
    # path('validate_discount_code/', views.validate_discount_code, name='validate_discount_code'),


    path('transfer/', views.transfer, name='transfer'),
    path('transfer_form/', views.transfer_form, name='transfer_form'),
    path('paypal_form/', views.paypal_form, name='paypal_form'),
    path('credit_form/', views.credit_form, name='credit_form'),
    path('bank_form/', views.bank_form, name='bank_form'),
    path('local_form/', views.local_form, name='local_form'),

    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('check_product_existence/', views.check_product_existence, name='check_product_existence'),
    path('get_product_details/', views.get_product_details, name='get_product_details'),
    # Pasarelas de pago Stripe
    path('charge/', views.charge, name='charge'),


    # Pasarelas de pago Paypal
    # path('payment/process/', views.payment_process, name='payment_process'),
    # path('payment/execute/', views.payment_execute, name='payment_execute'),
    # path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
] 
