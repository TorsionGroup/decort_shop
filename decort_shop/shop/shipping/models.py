from django.db import models
from datetime import datetime


class Region(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"


class DeliveryMethod(models.Model):
    code = models.CharField(max_length=250, null=True, blank=True)
    region_available = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=250)
    comment = models.TextField(null=True, blank=True)
    red = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DeliveryMethod"
        verbose_name_plural = "DeliveryMethods"


class DeliveryService(models.Model):
    name = models.CharField(max_length=250)
    has_to_door = models.BooleanField(default=0)
    parameters = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DeliveryService"
        verbose_name_plural = "DeliveryService"


class DeliveryCity(models.Model):
    service_id = models.ForeignKey(
        DeliveryService, on_delete=models.CASCADE, related_name="city_service", null=True, blank=True)
    region = models.CharField(max_length=250, null=True, blank=True)
    ref = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250)
    create_date = models.DateTimeField(default=datetime.today, null=True)
    update_date = models.DateTimeField(default=datetime.today, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DeliveryCity"
        verbose_name_plural = "DeliveryCities"


class DeliveryPoint(models.Model):
    service_id = models.ForeignKey(
        DeliveryService, on_delete=models.CASCADE, related_name="point_service", null=True, blank=True)
    city_id = models.ForeignKey(
        DeliveryCity, on_delete=models.CASCADE, related_name="point_city", null=True, blank=True)
    street = models.CharField(max_length=250, null=True, blank=True)
    ref = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.CharField(max_length=250, null=True, blank=True)
    max_weight = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DeliveryPoint"
        verbose_name_plural = "DeliveryPoints"



