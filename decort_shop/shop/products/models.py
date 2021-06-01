from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from ..models import *


class Cross(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cross_product", null=True, blank=True)
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="cross_brand", null=True, blank=True)
    article_nr = models.CharField(max_length=500, null=True, blank=True)
    search_nr = models.CharField(max_length=500, null=True, blank=True)
    product = models.CharField(max_length=500, null=True, blank=True)
    brand = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.article_nr

    class Meta:
        verbose_name = "Cross"
        verbose_name_plural = "Crosses"


class ProductApplicability(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="applicability_product", null=True, blank=True)
    vehicle = models.CharField(max_length=250, null=True, blank=True)
    modification = models.CharField(max_length=250, null=True, blank=True)
    engine = models.CharField(max_length=250, null=True, blank=True)
    year = models.CharField(max_length=250, null=True, blank=True)
    product = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "ProductApplicability"
        verbose_name_plural = "ProductApplicabilitys"


class ProductDescription(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="description_product", null=True, blank=True)
    property = models.CharField(max_length=500, null=True, blank=True)
    value = models.CharField(max_length=500, null=True, blank=True)
    product = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "ProductDescription"
        verbose_name_plural = "ProductDescriptions"


class Price(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="price_product", null=True, blank=True)
    price_type_id = models.ForeignKey(
        PriceType, on_delete=models.CASCADE, related_name="price_price_type", null=True, blank=True)
    currency_id = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="price_currency", null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=0)
    product = models.CharField(max_length=300, null=True, blank=True)
    price_type = models.CharField(max_length=300, null=True, blank=True)
    currency = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.price

    class Meta:
        verbose_name = "Price"
        verbose_name_plural = "Prices"


class Stock(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stock_product", null=True, blank=True)
    stock_name = models.CharField(max_length=300, default='Stock')
    amount_total = models.IntegerField(default=0, null=True)
    amount_account = models.IntegerField(default=0, null=True)
    product = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.amount_account

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class DeficitReserve(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="deficit_product", null=True, blank=True)
    sale_policy = models.CharField(max_length=250, null=True, blank=True)
    amount = models.IntegerField(default=0, null=True)
    product = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name = "DeficitReserve"
        verbose_name_plural = "DeficitReserves"


class ProductManufacturerModel(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="manufacturer_product", null=True, blank=True)
    product = models.CharField(max_length=300, null=True, blank=True)
    manufacturer_name = models.CharField(max_length=300, null=True, blank=True)
    model_name = models.CharField(max_length=300, null=True, blank=True)
    manufacturer_tecdoc_id = models.CharField(max_length=300, null=True, blank=True)
    model_tecdoc_id = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = "ProductManufacturerModel"
        verbose_name_plural = "ProductManufacturerModels"

