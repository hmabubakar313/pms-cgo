from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, PropertyManager, Listing, Image, Lead

admin.site.register(PropertyManager)
admin.site.register(CustomUser)
admin.site.register(Listing)
admin.site.register(Image)
admin.site.register(Lead)
