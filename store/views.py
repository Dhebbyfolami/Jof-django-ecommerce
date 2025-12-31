from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cart.cart import Cart
from .forms import CheckoutForm
from .models import Category, Product, Order, OrderItem


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    sort = request.GET.get("sort", "newest")
    if sort == "price_asc":
        products = products.order_by("price", "-created_at")
    elif sort == "price_desc":
        products = products.order_by("-price", "-created_at")
    else:
        products = products.order_by("-created_at")

    paginator = Paginator(products, 12)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    return render(
        request,
        "store/home.html",
        {
            "categories": categories,
            "category": category,
            "page_obj": page_obj,
            "q": q,
            "sort": sort,
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)
    return render(request, "store/product_detail.html", {"product": product})


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your cart is empty.")
        return redirect("store:product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order: Order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.is_paid = False
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()

            if order.payment_provider == "paystack":
                return redirect("payments:paystack_init", order_id=order.id)
            if order.payment_provider == "flutterwave":
                return redirect("payments:flutterwave_init", order_id=order.id)

            return redirect("store:order_success", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, "store/checkout.html", {"form": form, "cart": cart})


def order_success(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "store/order_success.html", {"order": order})
