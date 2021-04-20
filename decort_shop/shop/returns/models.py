from ..models import *
from ..customers.models import CustomerAgreement
from ..orders.models import Order


class ProformReturn(models.Model):
    source = models.CharField(max_length=300, null=True, blank=True)
    source_customer = models.CharField(max_length=300, null=True, blank=True)
    source_agreement = models.CharField(max_length=300, null=True, blank=True)
    source_order = models.CharField(max_length=300, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    agreement = models.ForeignKey(CustomerAgreement, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "ProformReturn"
        verbose_name_plural = "ProformReturns"

