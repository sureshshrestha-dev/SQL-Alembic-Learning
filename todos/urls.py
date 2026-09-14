from django.urls import path
from .views import todos, todo_detail

urlpatterns = [
    path('todos/', todos),
    path('todos/<int:id>/', todo_detail),
]