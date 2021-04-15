from django.db import models
from datetime import datetime
from ..models import Account
from ..products.models import Product


class Token(models.Model):
    user_id = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=datetime.today, null=True)
    type = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"


class PartnerApi(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=250, null=True, blank=True)
    token = models.CharField(max_length=250, null=True, blank=True)
    margin = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    percent_prepayment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    show_branch = models.BooleanField(default=1)
    enabled = models.BooleanField(default=0)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "PartnerApi"
        verbose_name_plural = "PartnerApis"


class CacheApi(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="cache_partner", null=True, blank=True)
    search_number = models.CharField(max_length=250)
    response_api = models.TextField(null=True, blank=True)
    response_date = models.DateTimeField(default=datetime.today, null=True)

    def __str__(self):
        return self.search_number

    class Meta:
        verbose_name = "CacheApi"
        verbose_name_plural = "CacheApis"


class PartnerApiCache(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="apicache_partner", null=True, blank=True)
    search_number = models.CharField(max_length=250, null=True, blank=True)
    response_date = models.DateTimeField(default=datetime.today, null=True)
    product_json = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.search_number

    class Meta:
        verbose_name = "PartnerApiCache"
        verbose_name_plural = "PartnerApiCaches"


class PartnerCategory(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="category_partner", null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, default=0, null=True)
    response_date = models.DateTimeField(default=datetime.today, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "PartnerCategory"
        verbose_name_plural = "PartnerCategories"


class CategoryMapping(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="mapping_partner", null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    category_id = models.ForeignKey(
        PartnerCategory, on_delete=models.CASCADE, related_name="mapping_category", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CategoryMapping"
        verbose_name_plural = "CategoryMappings"


class PartnerCategoryCache(models.Model):
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="category_cache_partner", null=True, blank=True)
    category_id = models.ForeignKey(
        PartnerCategory, on_delete=models.CASCADE, related_name="category_cache_category", null=True, blank=True)
    response_date = models.DateTimeField(default=datetime.today, null=True)
    product_json = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.response_date

    class Meta:
        verbose_name = "PartnerCategoryCache"
        verbose_name_plural = "PartnerCategoryCaches"


class PartnerStock(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_partner", null=True, blank=True)
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="stock_partner", null=True, blank=True)
    branch = models.CharField(max_length=250, null=True, blank=True)
    qty = models.IntegerField(default=0)
    supply_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.qty

    class Meta:
        verbose_name = "PartnerStock"
        verbose_name_plural = "PartnerStocks"


class ProductApiMap(models.Model):
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_api_map", null=True, blank=True)
    partner_code = models.ForeignKey(
        PartnerApi, on_delete=models.CASCADE, related_name="partner_api_map", null=True, blank=True)
    api_key = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.partner_code

    class Meta:
        verbose_name = "ProductApiMap"
        verbose_name_plural = "ProductApiMaps"

