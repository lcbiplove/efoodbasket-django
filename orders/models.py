from products.models import Product
from django.db import models
from django.contrib.auth import get_user_model
from carts.models import Voucher, CollectionSlot


class Payment(models.Model):
    type = models.CharField(max_length=255, default='PAYPAL')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    paypal_order_id = models.CharField(max_length=128)
    paypal_payer_id = models.CharField(max_length=128)
    payment_date = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    collection_date = models.DateField()
    ordered_date = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    collection_slot = models.ForeignKey(CollectionSlot, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, null=True)


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
