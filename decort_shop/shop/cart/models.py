from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import *


class Cart(models.Model):
    session = models.CharField("Сессия пользователя", max_length=500, null=True, blank=True)
    user = models.ForeignKey(
        Account, verbose_name='Покупатель', on_delete=models.CASCADE, null=True, blank=True
    )
    accepted = models.BooleanField(verbose_name='Принято к заказу', default=False)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return "{}".format(self.user)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, verbose_name='Корзина', on_delete=models.CASCADE, related_name="cart_item"
    )
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    price_sum = models.PositiveIntegerField("Общая сумма", default=0)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        self.price_sum = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.cart)


@receiver(post_save, sender=Account)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

