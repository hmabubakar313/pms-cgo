
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ui/', include('ui.urls')),
    path('user/', include('user.urls')),
]
