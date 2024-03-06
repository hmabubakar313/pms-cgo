from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import CustomUserManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("broker", "Broker"),
        ("property_manager", "Property Manager"),
        ("tenant", "Tenant"),
    )

    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class PropertyManager(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)
    username = models.CharField("username", max_length=100)

    def __str__(self):
        return self.username


class Listing(models.Model):
    property_manager = models.ForeignKey("PropertyManager", on_delete=models.CASCADE)
    Tenant = models.ForeignKey(
        "Tenant", on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    num_bedrooms = models.IntegerField(validators=[MinValueValidator(0)])
    num_bathrooms = models.IntegerField()
    square_footage = models.IntegerField()
    address = models.CharField(max_length=100)
    image = models.ManyToManyField("Image")

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to="image/")


class Broker(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)
    property_manager = models.ForeignKey("PropertyManager", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    commission_rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )


class Tenant(models.Model):
    user = models.OneToOneField(
        "CustomUser", related_name="tenant", on_delete=models.CASCADE
    )
    property_manager = models.ForeignKey(
        "PropertyManager", related_name="tenants", on_delete=models.CASCADE
    )
    broker = models.ForeignKey(
        "Broker",
        related_name="tenants",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class Lead(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    )

    datetime = models.DateTimeField()
    person_in_charge = models.EmailField(_("email address"), unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    tenant_met = models.OneToOneField(
        "Tenant", on_delete=models.CASCADE, blank=True, null=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lead on {self.date} (Status: {self.status})"


@receiver(post_save, sender=Lead)
def create_lead_history_on_save(sender, instance, created, **kwargs):
    if created:
        # If a new Lead instance is created, create a new LeadHistory instance
        LeadHistory.objects.create(
            lead=instance,
            meeting_datetime=instance.datetime,
            person_in_charge=instance.person_in_charge,
            status=instance.status,
            tenant_met=instance.tenant_met,
            notes=instance.notes,
        )
    else:
        # If an existing Lead instance is updated, create a new LeadHistory instance
        LeadHistory.objects.create(
            lead=instance,
            meeting_datetime=instance.datetime,
            person_in_charge=instance.person_in_charge,
            status=instance.status,
            tenant_met=instance.tenant_met,
            notes=instance.notes,
        )


@receiver(post_delete, sender=Lead)
def create_lead_history_on_delete(sender, instance, **kwargs):
    # If a Lead instance is deleted, create a new LeadHistory instance
    LeadHistory.objects.create(
        lead=instance,
        meeting_datetime=instance.datetime,
        person_in_charge=instance.person_in_charge,
        status=instance.status,
        tenant_met=instance.tenant_met,
        notes=instance.notes,
    )


class LeadHistory(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    meeting_datetime = models.DateTimeField()
    history_created_at = models.DateTimeField(auto_now_add=True)
    person_in_charge = models.EmailField(_("email address"))
    status = models.CharField(max_length=20, choices=Lead.STATUS_CHOICES)
    tenant_met = models.ForeignKey(
        "Tenant", on_delete=models.SET_NULL, blank=True, null=True
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Lead Histories"


class ContractAgreement(models.Model):
    commission_rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    broker = models.OneToOneField("Broker", on_delete=models.CASCADE)
    property_manager = models.ForeignKey("PropertyManager", on_delete=models.CASCADE)
    listing = models.OneToOneField("Listing", on_delete=models.CASCADE)
    tenant = models.OneToOneField("Tenant", on_delete=models.CASCADE)


class Document(models.Model):
    DOCUMENT_TYPES = (
        ("image", "Image"),
        ("pdf", "PDF"),
        ("agreement", "Agreement"),
    )
    contract_agreement = models.ForeignKey(
        "ContractAgreement", on_delete=models.CASCADE
    )
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to="documents/")

    def __str__(self):
        return self.title
