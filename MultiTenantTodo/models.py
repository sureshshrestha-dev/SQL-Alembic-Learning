# from django.db import models


# class Tenant(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class TodoItem(models.Model):
#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='todos')
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     is_completed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title
