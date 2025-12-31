from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("category/<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("product/<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:order_id>/success/", views.order_success, name="order_success"),
]
