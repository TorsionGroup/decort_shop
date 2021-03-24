from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'agreement_id', 'delivery_method', 'point_id', 'order_number', 'paid')
    list_display_links = ('id', 'user_id', 'agreement_id', 'delivery_method', 'order_number',)
    search_fields = ('user_id', 'delivery_method', 'order_number',)
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(OrderPayment)
admin.site.register(DropshippingWallet)
admin.site.register(DropshippingWalletTransfer)
