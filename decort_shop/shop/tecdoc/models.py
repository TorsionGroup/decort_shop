from django.db import models
from datetime import datetime
from ..models import *


class Manufacturer(models.Model):
    source = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    manufacturer_tecdoc_id = models.CharField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    canbedisplayed = models.BooleanField(default=0, null=True, blank=True)
    ispassengercar = models.BooleanField(default=0, null=True, blank=True)
    iscommercialvehicle = models.BooleanField(default=0, null=True, blank=True)
    ismotorbike = models.BooleanField(default=0, null=True, blank=True)
    isengine = models.BooleanField(default=0, null=True, blank=True)
    isaxle = models.BooleanField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"


class ManufacturerModel(models.Model):
    source = models.CharField(max_length=300, null=True, blank=True)
    source_manufacturer = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    constructioninterval = models.CharField(max_length=300, null=True, blank=True)
    model_tecdoc_id = models.CharField(max_length=300, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True)
    manufacturer_tecdoc_id = models.CharField(max_length=300, null=True, blank=True)
    canbedisplayed = models.BooleanField(default=0, null=True, blank=True)
    ispassengercar = models.BooleanField(default=0, null=True, blank=True)
    iscommercialvehicle = models.BooleanField(default=0, null=True, blank=True)
    ismotorbike = models.BooleanField(default=0, null=True, blank=True)
    isengine = models.BooleanField(default=0, null=True, blank=True)
    isaxle = models.BooleanField(default=0, null=True, blank=True)
    commercial = models.BooleanField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ManufacturerModel"
        verbose_name_plural = "ManufacturerModels"

