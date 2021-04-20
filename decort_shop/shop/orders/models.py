from django.db import models
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField
from ..models import *
from ..customers.models import CustomerAgreement, CustomerPoint
from ..shipping.models import DeliveryMethod, DeliveryService, DeliveryCity, DeliveryPoint


class Order(models.Model):
    user_id = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    agreement_id = models.ForeignKey(
        CustomerAgreement, on_delete=models.SET_NULL, related_name="order_agreement", null=True, blank=True)
    complete = models.BooleanField(default=0, null=True, blank=True)
    delivery_method = models.ForeignKey(
        DeliveryMethod, on_delete=models.SET_NULL, related_name="order_delivery", null=True, blank=True)
    order_date = models.CharField(max_length=300, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    point_id = models.ForeignKey(
        CustomerPoint, on_delete=models.SET_NULL, related_name="order_customer_point", null=True, blank=True)
    delivery_service_id = models.ForeignKey(
        DeliveryService, on_delete=models.SET_NULL, related_name="order_del_point", null=True, blank=True)
    delivery_city_id = models.ForeignKey(
        DeliveryCity, on_delete=models.SET_NULL, related_name="order_del_city", null=True, blank=True)
    delivery_point_id = models.ForeignKey(
        DeliveryPoint, on_delete=models.SET_NULL, related_name="order_del_point", null=True, blank=True)
    delivery_contact = models.CharField(max_length=250, null=True, blank=True)
    delivery_contact_phone = PhoneNumberField(blank=True, null=True)
    order_number = models.CharField(max_length=250, null=True, blank=True)
    waybill_number = models.CharField(max_length=250, null=True, blank=True)
    invoice_number = models.CharField(max_length=250, null=True, blank=True)
    order_source = models.CharField(max_length=300, null=True, blank=True)
    is_pay_on_delivery = models.BooleanField(default=0, null=True)
    pay_on_delivery_sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    import_reason = models.TextField(null=True, blank=True)
    import_status = models.CharField(max_length=250, null=True, blank=True)
    partner_code = models.CharField(max_length=250, null=True, blank=True)
    declared_sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    declared_currency = models.BooleanField(default=1, null=True)
    source_type = models.CharField(max_length=250, default='B2B', null=True)
    delivery_contact_surname = models.CharField(max_length=250, null=True, blank=True)
    delivery_contact_middlename = models.CharField(max_length=250, null=True, blank=True)
    delivery_is_invoice_off = models.BooleanField(default=1, null=True, blank=True)
    agreement = models.CharField(max_length=300, null=True, blank=True)
    has_precept = models.BooleanField(default=0, null=True, blank=True)
    has_waybill = models.BooleanField(default=0, null=True, blank=True)
    paid = models.BooleanField(default=False, null=True, blank=True)
    declaration_number = models.CharField(max_length=250, null=True, blank=True)
    declaration_number_status = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ('-created',)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_item_order", null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_item_product", null=True, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="order_item_currency", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True)
    order_source = models.CharField(max_length=300, null=True, blank=True)
    reserved = models.IntegerField(default=0, null=True)
    executed = models.IntegerField(default=0, null=True)
    old_qty = models.IntegerField(null=True, blank=True)
    old_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    update_date = models.DateTimeField(null=True, blank=True)
    purchase_qty = models.IntegerField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    purchase_currency_id = models.IntegerField(null=True, blank=True)
    purchase_order_id = models.IntegerField(null=True, blank=True)
    purchase_item_id = models.IntegerField(null=True, blank=True)
    partner_branch = models.CharField(max_length=300, null=True, blank=True)
    product_source = models.CharField(max_length=300, null=True, blank=True)
    currency_source = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"


class OrderPayment(models.Model):
    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_payment_order", null=True, blank=True)
    sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    date_payment = models.DateTimeField(default=datetime.today, null=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="order_payment_currency", null=True, blank=True)
    payment_sum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    receiver_commission = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sender_commission = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.order_id

    class Meta:
        verbose_name = "OrderPayment"
        verbose_name_plural = "OrderPayments"


class OrderSourceStatistic(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_statistic_product", null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="order_statistic_customer", null=True, blank=True)
    source_type = models.CharField(max_length=250, null=True, blank=True)
    add_date = models.DateTimeField(default=datetime.today, null=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "OrderSourceStatistic"
        verbose_name_plural = "OrderSourceStatistics"
