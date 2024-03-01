
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('dashboard/',views.dashboard,name="dashboard"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('table/',views.table,name="table")
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)