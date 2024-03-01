from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class PropertyManager(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    username = models.CharField("username", max_length=100)

    def __str__(self):
        return self.username


class Listing(models.Model):
    property_manager = models.ForeignKey('PropertyManager', on_delete=models.CASCADE)
    # Tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    num_bedrooms = models.IntegerField(  validators=[MinValueValidator(0)])
    num_bathrooms = models.IntegerField()
    square_footage = models.IntegerField()
    address = models.CharField(max_length=100)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='image/')

# class Brokers(CustomUser):
#     property_manager = models.ForeignKey('PropertyManager', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)


# class Tenant(CustomUser):
#     property_manager = models.ForeignKey('PropertyManager', on_delete=models.CASCADE)
#     broker = models.ForeignKey('Broker', on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)


# class Leads(models.Model):
#     date = models.DateField()
    