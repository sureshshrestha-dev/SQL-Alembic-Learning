from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("supervisor", "Supervisor"),
        ("agent", "Agent"),
    ]

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="users"
    )
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="agent"
    )
    # username = models.CharField(max_length=150, unique=False,default="testuser", blank=False, null=False)
    # email = models.EmailField(unique=True)
    # phone_number = models.CharField(max_length=20, blank=True, null=True)
    # password = models.CharField(max_length=128, blank=False, null=False,default="testpassword")
