
from django.contrib import admin
from django.urls import path,include
from ui import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ui/', include(urls)),

]
