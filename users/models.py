from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, fullname, contact, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            contact=contact,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, contact, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            fullname=fullname,
            contact=contact,
        )
        user.user_role = User.USER_IS_ADMIN
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    USER_IS_CUSTOMER = 'CUSTOMER'
    USER_IS_TRADER = 'TRADER'
    USER_IS_ADMIN = 'ADMIN'
    USER_TYPE_CHOICES = [
        (USER_IS_CUSTOMER, 'Customer'),
        (USER_IS_TRADER, 'Trader'),
        (USER_IS_ADMIN, 'Admin'),
    ]

    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=48)
    address = models.CharField(max_length=48)
    user_role = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=USER_IS_CUSTOMER)
    contact = models.IntegerField()
    joined_date = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(null=True)
    token = models.CharField(null=True, max_length=48)
    otp_last_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'contact']

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        return self.USER_IS_ADMIN == self.user_role

class Trader(models.Model):
    APPROVAL_IS_SUCCESS = 'Y'
    APPROVAL_IS_PENDING = 'P'
    APPROVAL_IS_FAIL = 'N'
    APPROVAL_CHOICES = [
        (APPROVAL_IS_SUCCESS, 'Approved'),
        (APPROVAL_IS_PENDING, 'Pending'),
        (APPROVAL_IS_FAIL, 'Rejected'),
    ]

    pan = models.CharField(unique=True, max_length=12)
    product_type = models.CharField(unique=True, max_length=30)
    product_details = models.TextField(max_length=4000)
    documents_path = models.TextField(max_length=1000)
    is_approved = models.CharField(default=APPROVAL_IS_PENDING, choices=APPROVAL_CHOICES, max_length=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email}"