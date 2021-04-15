from django.db import models
from datetime import datetime
from creditcards.models import CardNumberField
from ..products.models import Currency
from ..customers.models import CustomerAgreement
from ..orders.models import Order


class DropshippingWallet(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="d_wallet_order", null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="d_wallet_agreement", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="d_wallet_currency", null=True, blank=True)
    debit = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    order_order = models.CharField(max_length=300, null=True, blank=True)
    agreement = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name = "DropshippingWallet"
        verbose_name_plural = "DropshippingWallets"


class DropshippingWalletTransfer(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="d_transfer_order", null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="d_transfer_agreement", null=True, blank=True)
    sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="d_transfer_currency", null=True, blank=True)
    date = models.DateTimeField(default=datetime.today, null=True)
    card = CardNumberField(null=True, blank=True)

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name = "DropshippingWalletTransfer"
        verbose_name_plural = "DropshippingWalletTransfers"

