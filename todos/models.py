from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class TodoCategory(models.Model):
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="todo_categories"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_todo_categories"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "slug"],
                name="unique_todo_category_slug_per_tenant"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or "category"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Todo(models.Model):
    TODO_TYPE_CHOICES = [
        ("personal", "Personal"),
        ("shared", "Shared"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("not_complete", "Not Complete"),
        ("complete", "Complete"),
        ("postponed", "Postponed"),
        ("cancelled", "Cancelled"),
    ]

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
    todo_type = models.CharField(max_length=20, choices=TODO_TYPE_CHOICES, default="shared")
    category = models.ForeignKey(
        "TodoCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="todos"
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_complete")
    review_comment = models.TextField(blank=True, default="")
    satisfaction = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.is_completed = self.status == "complete"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title