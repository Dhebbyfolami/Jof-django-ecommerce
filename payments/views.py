import os
import uuid
import requests
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from store.models import Order


def _site_url(request):
    # Build absolute base URL for redirects (works on Render/Heroku/most platforms)
    scheme = "https" if request.is_secure() else "http"
    host = request.get_host()
    return f"{scheme}://{host}"


def paystack_init(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)

    secret = os.environ.get("PAYSTACK_SECRET_KEY")
    if not secret:
        messages.error(request, "PAYSTACK_SECRET_KEY is not set on the server.")
        return redirect("store:order_success", order_id=order.id)

    if not order.payment_reference:
        order.payment_reference = f"JOF-{order.id}-{uuid.uuid4().hex[:10]}"
        order.save(update_fields=["payment_reference"])

    callback_url = _site_url(request) + reverse("payments:paystack_verify")
    payload = {
        "email": order.email,
        "amount": int(order.total_amount * 100),  # kobo
        "reference": order.payment_reference,
        "callback_url": callback_url,
    }

    r = requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=payload,
        headers={"Authorization": f"Bearer {secret}"},
        timeout=30,
    )
    if r.status_code >= 400:
        return HttpResponseBadRequest("Paystack initialize failed.")

    data = r.json().get("data") or {}
    auth_url = data.get("authorization_url")
    if not auth_url:
        return HttpResponseBadRequest("Paystack response missing authorization_url.")

    return redirect(auth_url)


def paystack_verify(request):
    reference = request.GET.get("reference", "").strip()
    if not reference:
        return HttpResponseBadRequest("Missing reference.")

    secret = os.environ.get("PAYSTACK_SECRET_KEY")
    if not secret:
        return HttpResponseBadRequest("PAYSTACK_SECRET_KEY not set.")

    order = get_object_or_404(Order, payment_reference=reference)

    r = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers={"Authorization": f"Bearer {secret}"},
        timeout=30,
    )
    if r.status_code >= 400:
        messages.error(request, "Payment verification failed.")
        return redirect("store:order_success", order_id=order.id)

    data = r.json().get("data") or {}
    status = data.get("status")
    if status == "success":
        order.is_paid = True
        order.save(update_fields=["is_paid"])
        messages.success(request, "Payment successful. Thank you!")
    else:
        messages.warning(request, "Payment not completed.")

    return redirect("store:order_success", order_id=order.id)


def flutterwave_init(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    secret = os.environ.get("FLUTTERWAVE_SECRET_KEY")
    if not secret:
        messages.error(request, "FLUTTERWAVE_SECRET_KEY is not set on the server.")
        return redirect("store:order_success", order_id=order.id)

    if not order.payment_reference:
        order.payment_reference = f"JOF-{order.id}-{uuid.uuid4().hex[:10]}"
        order.save(update_fields=["payment_reference"])

    redirect_url = _site_url(request) + reverse("payments:flutterwave_verify")
    payload = {
        "tx_ref": order.payment_reference,
        "amount": str(order.total_amount),
        "currency": "NGN",
        "redirect_url": redirect_url,
        "customer": {"email": order.email, "name": order.full_name, "phonenumber": order.phone},
        "customizations": {"title": "Jof", "description": f"Order #{order.id}"},
    }

    r = requests.post(
        "https://api.flutterwave.com/v3/payments",
        json=payload,
        headers={"Authorization": f"Bearer {secret}"},
        timeout=30,
    )
    if r.status_code >= 400:
        return HttpResponseBadRequest("Flutterwave initialize failed.")

    data = r.json().get("data") or {}
    link = data.get("link")
    if not link:
        return HttpResponseBadRequest("Flutterwave response missing payment link.")
    return redirect(link)


def flutterwave_verify(request):
    status = request.GET.get("status", "").strip()
    tx_ref = request.GET.get("tx_ref", "").strip()

    if not tx_ref:
        return HttpResponseBadRequest("Missing tx_ref.")

    order = get_object_or_404(Order, payment_reference=tx_ref)

    if status == "successful":
        order.is_paid = True
        order.save(update_fields=["is_paid"])
        messages.success(request, "Payment successful. Thank you!")
    elif status == "cancelled":
        messages.warning(request, "Payment cancelled.")
    else:
        messages.warning(request, "Payment not completed.")

    return redirect("store:order_success", order_id=order.id)
