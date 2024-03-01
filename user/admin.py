from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, PropertyManager


class PropertyManagerAdmin(UserAdmin):
    pass  # Customize admin options if needed


admin.site.register(PropertyManager, PropertyManagerAdmin)
