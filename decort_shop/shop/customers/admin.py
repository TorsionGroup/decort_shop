from django.contrib import admin
from .models import *


@admin.register(CustomerAgreement)
class CustomerAgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'customer_id', 'code', 'number', 'currency_id')
    list_display_links = ('name', 'customer_id',)
    search_fields = ('name', 'customer_id',)


admin.site.register(CustomerDiscount)
admin.site.register(CustomerPoint)
admin.site.register(Balance)
