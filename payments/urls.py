from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("paystack/init/<int:order_id>/", views.paystack_init, name="paystack_init"),
    path("paystack/verify/", views.paystack_verify, name="paystack_verify"),
    path("flutterwave/init/<int:order_id>/", views.flutterwave_init, name="flutterwave_init"),
    path("flutterwave/verify/", views.flutterwave_verify, name="flutterwave_verify"),
]
