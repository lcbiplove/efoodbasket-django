from django.db.models.fields import FloatField
from users.models import Trader, User
from django.db import models
from django.urls import reverse
from . import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db.models import F, Avg, Count
from django.db.models.functions import Round, Coalesce
from operator import itemgetter, mod

import products

class Shop(models.Model):
    name = models.CharField(max_length=40, validators=[validators.validate_shop_name])               
    address = models.CharField(max_length=40, validators=[validators.validate_address])     
    contact = models.IntegerField(validators=[validators.validate_contact])
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'trader'], name='unique_for_trader')
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('shop_list')

    def clean_fields(self, exclude) -> None:
        qs = Shop.objects.filter(name__icontains=self.name, trader__id=self.trader.id)
        if qs.exists():
            raise ValidationError({'name':[ 'Shop of the same name already exist',]})
        return super().clean_fields(exclude=exclude)


    @property
    def beautify_contact(self):
        contact = str(self.contact)
        phone = format(int(contact[:-1]), ",").replace(",", "-") + contact[-1]
        return phone


class ProductCategory(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.TextField(max_length=2000)

    class Meta:
        verbose_name_plural = 'Product Categories'    

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, validators=[MinLengthValidator(3)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    availability = models.BooleanField(default=True)
    description = models.TextField(max_length=2000, validators=[MinLengthValidator(100)])
    allergy_information = models.TextField(max_length=2000, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_date',]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.id})

    def thumbnail_url(self):
        return self.product_images.all().first()

    def get_similar_products(self):
        return Product.objects.filter(category__id=self.category.id).exclude(id=self.id)[:4]

    def is_in_wish_list(self):
        return False

    def reviews(self):
        return Review.objects.filter(rating__product__id=self.id ).select_related('rating', 'rating__product', 'rating__user' ) 

    def rating(self):
        rating = Rating.objects.filter(product__id=self.id).\
                aggregate(rating=Coalesce(
                    Avg('rating'), 0, output_field=FloatField()
                    )
                )['rating']
        return round(rating, 2)

    def analyze_rating(self):
        queryset = Rating.objects.filter(product__id=self.id)
        total = queryset.count()
        qs = queryset.annotate(
                rate=Round('rating')
            ).values('rate').annotate(total=Count('rate'))

        qs_list = list(qs)

        for item in qs_list:
            item['percent'] = item['total'] / total * 100

        for i in range(1, 6):
            if not any(int(d['rate']) == i for d in qs_list):
                qs_list.append(
                    {
                        'rate': i,
                        'total': 0,
                        'percent': 0,
                    }
                )
        newlist = sorted(qs_list, key=itemgetter('rate'), reverse=True) 
        return newlist

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/')

    def __str__(self) -> str:
        return self.image.url

class Query(models.Model):
    question = models.CharField(max_length=2000, validators=[MinLengthValidator(10)])
    answer = models.CharField(max_length=2000, null=True, blank=True)
    question_date = models.DateTimeField(auto_now_add=True)
    answer_date = models.DateTimeField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Queries'
        ordering = [F('answer').asc(nulls_last=True), '-question_date', '-answer_date']

    def __str__(self) -> str:
        return self.question

    def is_answered(self):
        return self.answer


class Rating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    added_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_for_rating')
        ]

    def __str__(self) -> str:
        return str(self.rating)
    

class Review(models.Model):
    review = models.CharField(max_length=2000, validators=[MinLengthValidator(10)])
    added_date = models.DateTimeField(auto_now_add=True)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, unique=True)

    def __str__(self) -> str:
        return self.review


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wishlists')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_for_user')
        ]

    def __str__(self) -> str:
        return self.user.email+ " / " + self.product.name
