from django.db import models
from creditcards.models import CardNumberField
from ..models import *


class CustomerAgreement(models.Model):
    code = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300)
    number = models.CharField(max_length=300, null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="agreement_customer", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="agreement_currency", null=True, blank=True)
    price_type_id = models.ForeignKey(
        PriceType, on_delete=models.CASCADE, related_name="agreement_price_type", null=True, blank=True)
    is_status = models.BooleanField(default=1, null=True)
    discount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=1, null=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    api_available = models.BooleanField(default=0, null=True)
    api_token = models.CharField(max_length=300, null=True, blank=True)
    customer = models.CharField(max_length=300, null=True, blank=True)
    currency = models.CharField(max_length=300, null=True, blank=True)
    price_type = models.CharField(max_length=300, null=True, blank=True)
    finish_date = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CustomerAgreement"
        verbose_name_plural = "CustomerAgreements"


class CustomerCard(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=300)
    card = CardNumberField()

    def __str__(self):
        return self.card

    class Meta:
        verbose_name = "CustomerCard"
        verbose_name_plural = "CustomerCard"


class CustomerContact(models.Model):
    source = models.CharField(max_length=300, null=True, blank=True)
    source_customer = models.CharField(max_length=300, null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="contact_customer", null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=300, null=True, blank=True)
    is_user = models.BooleanField(default=1, null=True, blank=True)
    birthday = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CustomerContact"
        verbose_name_plural = "CustomerContacts"


class CustomerDiscount(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="discount_customer_customer", null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="discount_customer_agreement", null=True, blank=True)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    criteria_type = models.CharField(max_length=300, null=True, blank=True)
    discount = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    price_type_id = models.ForeignKey(
        PriceType, on_delete=models.CASCADE, related_name="discount_customer_price_type", null=True, blank=True)
    customer = models.CharField(max_length=300, null=True, blank=True)
    agreement = models.CharField(max_length=300, null=True, blank=True)
    price_type = models.CharField(max_length=300, null=True, blank=True)
    brand = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "CustomerDiscount"
        verbose_name_plural = "CustomerDiscounts"


class CustomerPoint(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="point_customer")
    name = models.CharField(max_length=500)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    add = models.CharField(max_length=500, null=True, blank=True)
    customer = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.CharField(max_length=500, null=True, blank=True)
    longitude = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CustomerPoint"
        verbose_name_plural = "CustomerPoints"


class CustomerPointGPS(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="point_gps_customer")
    name = models.CharField(max_length=500)
    source_id = models.CharField(max_length=300, null=True, blank=True)
    add_name = models.CharField(max_length=500, null=True, blank=True)
    customer = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.CharField(max_length=500, null=True, blank=True)
    longitude = models.CharField(max_length=500, null=True, blank=True)
    extra_name = models.CharField(max_length=500, null=True, blank=True)
    area_ref = models.CharField(max_length=300, null=True, blank=True)
    city_ref = models.CharField(max_length=300, null=True, blank=True)
    street_type_ref = models.CharField(max_length=300, null=True, blank=True)
    street_ref = models.CharField(max_length=300, null=True, blank=True)
    extra_street = models.CharField(max_length=300, null=True, blank=True)
    house_number = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CustomerPoint"
        verbose_name_plural = "CustomerPoints"


class Balance(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="balance_customer", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="balance_currency", null=True, blank=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    past_due = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.CASCADE, related_name="balance_agreement", null=True, blank=True)
    customer = models.CharField(max_length=300, null=True, blank=True)
    currency = models.CharField(max_length=300, null=True, blank=True)
    agreement = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.balance

    class Meta:
        verbose_name = "Balance"
        verbose_name_plural = "Balances"


