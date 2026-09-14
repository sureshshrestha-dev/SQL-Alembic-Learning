from django.urls import path
from .views import tenants, tenant_detail

urlpatterns = [
    path('tenants/', tenants),
    path('tenants/<int:id>/', tenant_detail),
]