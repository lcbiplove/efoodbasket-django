from django.contrib import admin
from . import models

admin.site.register(models.Shop)
admin.site.register(models.ProductCategory)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)