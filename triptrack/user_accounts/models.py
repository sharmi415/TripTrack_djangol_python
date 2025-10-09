from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# --- Custom User Model ---
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("developer_admin", "Developer Admin"),
        ("user_admin", "User Admin"),
        ("user", "User"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return self.username

# --- Hire Model ---
class Hire(models.Model):
    """
    Tracks when a User Admin hires the website for a limited period.
    """
    user_admin = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'user_admin'},
        related_name='hires'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    paid = models.BooleanField(default=False)

    def duration_days(self):
        return max((self.end_date - self.start_date).days, 0)

    def __str__(self):
        return f"{self.user_admin.username} hire from {self.start_date} to {self.end_date}"
