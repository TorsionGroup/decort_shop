from django.contrib import admin
from .models import *


admin.site.register(Stock)
admin.site.register(Cross)
admin.site.register(ProductApplicability)
admin.site.register(ProductDescription)

