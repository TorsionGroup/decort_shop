from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from ..models import *


class Sale(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale_product", null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    date = models.CharField(max_length=500, null=True, blank=True)
    product = models.CharField(max_length=500, null=True, blank=True)
    customer = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"


class SaleTask(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale_task_product", null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    product = models.CharField(max_length=500, null=True, blank=True)
    customer = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "SaleTask"
        verbose_name_plural = "SaleTasks"


class SaleHistory(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale_history_product", null=True, blank=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "SaleHistory"
        verbose_name_plural = "SaleHistories"


class SaleProductRelated(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sale_related_product", null=True, blank=True)
    related_product_id = models.IntegerField(null=True, blank=True)
    qty_index = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    calculation_type = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "SaleProductRelated"
        verbose_name_plural = "SaleProductRelateds"

