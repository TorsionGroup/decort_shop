from ..models import *


class PromoSale(models.Model):
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="promo_sale_customer", null=True, blank=True)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="promo_sale_product", null=True, blank=True)
    type = models.CharField(max_length=300, null=True, blank=True)
    is_visible = models.BooleanField(default=0)
    comment = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.product_id

    class Meta:
        verbose_name = "PromoSale"
        verbose_name_plural = "PromoSales"

