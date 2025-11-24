# events/forms.py
from django import forms
from .models import Payment

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method', 'payment_proof']
