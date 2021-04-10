from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from ..models import *


class Cart(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    in_order = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.cart)

    class Meta:
        verbose_name = 'Cart Product'
        verbose_name_plural = 'Cart Products'

