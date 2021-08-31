from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from random import randint
from django.utils import timezone
from django.forms import ModelForm


class UserManager(BaseUserManager):
    def create_user(
            self, email, fullname,
            contact,
            address=None,
            user_role=None,
            password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            address=address,
            user_role=user_role,
            contact=contact,
        )
        user.set_password(password)
        user.otp = randint(100000, 999999)
        user.otp_last_date = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email, fullname, contact, address=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            fullname=fullname,
            contact=contact,
            address=address
        )
        user.user_role = User.USER_IS_ADMIN
        user.is_active = True
        self.otp = randint(100000, 999999)
        self.otp_last_date = timezone.now()
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
    user_role = models.CharField(
                max_length=20,
                choices=USER_TYPE_CHOICES, default=USER_IS_CUSTOMER)
    contact = models.IntegerField()
    joined_date = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(null=True)
    otp_last_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)

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

    @property
    def is_trader(self):
        return self.USER_IS_TRADER == self.user_role

    @property
    def valid_otp(self):
        if self.otp_expired:
            self.otp = randint(100000, 999999)
            self.otp_last_date = timezone.now()
            self.save()
        return self.otp

    @property
    def otp_expired(self):
        diff = timezone.now() - self.otp_last_date
        return diff.seconds > 60*5

    @property
    def beautify_contact(self):
        # $num = '('.substr($phone_number, 0, 3).') '.substr($phone_number, 3, 3).'-'.substr($phone_number,6)
        contact = str(self.contact)
        phone = format(int(contact[:-1]), ",").replace(",", "-") + contact[-1]
        return phone

    @property
    def can_login(self):
        return self.is_active == True


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
    status = models.CharField(
        default=APPROVAL_IS_PENDING, choices=APPROVAL_CHOICES, max_length=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email}"

    @property
    def is_approved(self):
        return self.status == self.APPROVAL_IS_SUCCESS


class TraderDocument(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE, related_name='documents')
    document = models.ImageField(upload_to='documents/')


class TraderDocumentForm(ModelForm):
    class Meta:
        model = TraderDocument
        fields = ('document', )
        error_messages = {
            'document': {
                'required': "Please choose at least one file.",
            },
        }