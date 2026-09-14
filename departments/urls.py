from django.urls import path
from .views import departments, department_detail

urlpatterns = [
    path('departments/', departments),
    path('departments/<int:id>/', department_detail),
]