from django import forms
from .models import *


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []

