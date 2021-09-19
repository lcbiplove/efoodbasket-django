from products.models import Product
from django.db import models
from django.db.models import Sum
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

    def thumbnail_url(self):
        return self.order_product.all().first().product.thumbnail_url()

    def items_count(self):
        return self.order_product.all().aggregate(total=Sum('quantity'))['total']

    def subtotal(self):
        discount = self.voucher and self.voucher.discount or 0
        total = self.payment.amount
        subtotal =  float(total) * 100 / (100 - float(discount))
        return subtotal


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_order')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_product')

    def total(self):
        total = (100 - self.product.discount) * self.product.price/100*self.quantity
        return total
