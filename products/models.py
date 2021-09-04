from users.models import Trader, User
from django.db import models
from django.urls import reverse
from . import validators
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

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
        ordering = ['-question_date', '-answer_date']

    def __str__(self) -> str:
        return self.question

    def is_answered(self):
        return self.answer

    

class Review(models.Model):
    review = models.CharField(max_length=2000, validators=[MinLengthValidator(10)])
    added_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    product = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reviews')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_for_review')
        ]

class Rating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    added_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    product = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_ratings')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_for_rating')
        ]
