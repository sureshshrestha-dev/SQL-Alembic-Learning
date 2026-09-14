from django.urls import path
from .views import todo_categories, todo_category_detail, todos, todo_detail

urlpatterns = [
    path('todo-categories/', todo_categories),
    path('todo-categories/<int:id>/', todo_category_detail),
    path('todos/', todos),
    path('todos/<int:id>/', todo_detail),
]