from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/',views.dashboard,name="dashboard"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('listing/',views.listing,name="listing"),
    path('create_listing/',views.create_listing,name="create_listing"),
    path('view_list/<int:list_id>',views.view_list,name="view_list"),
    path('delete_listing/<int:list_id>',views.delete_listing,name="delete_listing"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)