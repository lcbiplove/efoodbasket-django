from django.contrib import admin
from .models import Cart, CollectionSlot, Voucher

admin.site.register(Voucher)
admin.site.register(Cart)
admin.site.register(CollectionSlot)

