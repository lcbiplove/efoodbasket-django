from users.models import Trader
from django.db import models
from django.urls import reverse
from . import validators

class Shop(models.Model):
    name = models.CharField(max_length=40, validators=[validators.validate_shop_name])               
    address = models.CharField(max_length=40, validators=[validators.validate_address])     
    contact = models.IntegerField(validators=[validators.validate_contact])
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('shop_list')

    @property
    def beautify_contact(self):
        # $num = '('.substr($phone_number, 0, 3).') '.substr($phone_number, 3, 3).'-'.substr($phone_number,6)
        contact = str(self.contact)
        phone = format(int(contact[:-1]), ",").replace(",", "-") + contact[-1]
        return phone


class ProductCategory(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=2000)

    class Meta:
        verbose_name_plural = 'Product Categories'    

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    availability = models.BooleanField(default=True)
    description = models.TextField(max_length=2000)
    allergy_information = models.TextField(max_length=2000, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name