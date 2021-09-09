from django.db import models
from users.models import User
from products.models import Product
from django.db.models import Sum


class Cart(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product.name} {self.user.email}"

    @staticmethod
    def get_carts_count(user):
        return Cart.objects.filter(user__id=user.id).aggregate(total=Sum('quantity'))['total'] or 0

class CollectionSlot(models.Model):
    day = models.CharField(max_length=20)
    shift = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.day} {self.shift}"