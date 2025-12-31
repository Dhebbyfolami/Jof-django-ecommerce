from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "payment_provider",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone (optional)"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Delivery address"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Country"}),
            "payment_provider": forms.Select(attrs={"class": "form-select"}),
        }
