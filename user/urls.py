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
    path('update_listing/<int:list_id>',views.update_listing,name="update_listing"),
    path('create_lead/',views.create_lead,name="create_lead"),
    path('list_leads/',views.list_leads,name="list_leads"),
    path('update_lead/<lead_id>/',views.update_lead,name="update_lead"),
    path('delete_lead/<lead_id>/',views.delete_lead,name="delete_lead"),
    path('create_tenant/',views.create_tenant,name="create_tenant"),
    path('list_tenants/',views.list_tenants,name="list_tenants"),
    path('delete_tenant/<tenant_id>/',views.delete_tenant,name="delete_tenant"),
    path('update_tenant/<tenant_id>/',views.update_tenant,name="update_tenant"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)