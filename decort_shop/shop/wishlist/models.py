from django.db import models
from datetime import datetime
from django.core.mail import send_mail

from ..models import Product, Account


class Wishlist(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.SET_NULL, related_name="wait_list_product", null=True, blank=True)
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    date_add = models.DateTimeField(default=datetime.today, null=True, blank=True)
    send_message = models.BooleanField(default=0)
    is_active = models.BooleanField(default=0)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

