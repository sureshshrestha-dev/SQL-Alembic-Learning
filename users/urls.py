from django.urls import path

from .views import login, logout, me, register, user_detail, users

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('me/', me),
    path('logout/', logout),
    path('users/', users),
    path('users/<int:id>/', user_detail),
]