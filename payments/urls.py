from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create/', views.CreatePaymentView.as_view(), name='create_payment'),
    path('webhook/', views.mercadopago_webhook, name='mercadopago_webhook'),
]
