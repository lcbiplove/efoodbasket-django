from django.contrib import admin
from . import models

admin.site.register(models.Shop)
admin.site.register(models.ProductCategory)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.Query)
admin.site.register(models.Rating)
admin.site.register(models.Review)