from django.db import models

class Todo(models.Model):
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="todos"
    )
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="todos"
    )
    assigned_to = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="assigned_todos"
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_todos"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title