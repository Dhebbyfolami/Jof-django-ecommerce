from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .cart import Cart

def detail(request):
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    override = request.POST.get("override") == "1"
    cart.add(product=product, quantity=1, override_quantity=False)
    return redirect("cart:detail")  

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:detail")  

def cart_decrease(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product)
    return redirect("cart:detail")