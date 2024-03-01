from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, PropertyManager,Listing,Image


# class PropertyManagerAdmin(UserAdmin):
#     pass  # Customize admin options if needed


admin.site.register(PropertyManager)
admin.site.register(CustomUser)
admin.site.register(Listing)
admin.site.register(Image)

