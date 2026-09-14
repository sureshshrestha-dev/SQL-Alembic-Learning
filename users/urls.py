from django.urls import path
from .views import user_detail, users

urlpatterns = [
    path('users/', users),
    path('users/<int:id>/', user_detail),
]