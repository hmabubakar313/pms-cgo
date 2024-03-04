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
    Tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE, blank=True, null=True)
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


class Brokers(models.Model):
    property_manager = models.ForeignKey('PropertyManager', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Tenant(models.Model):
    property_manager = models.ForeignKey('PropertyManager', on_delete=models.CASCADE)
    broker = models.ForeignKey('Brokers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Lead(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )

    date = models.DateField()
    person_in_charge = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    tenant_met = models.OneToOneField('Tenant',on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Lead on {self.date} (Status: {self.status})"
