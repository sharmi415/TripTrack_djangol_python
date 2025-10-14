from django.db import models
from django.conf import settings
from datetime import date

# === Roles ===
ROLE_CHOICES = [
    ('developer_admin', 'Developer Admin'),
    ('user_admin', 'User Admin'),
    ('creator', 'Creator'),      # Creator user
    ('enjoyer', 'Enjoyer'),      # Normal user / tour enjoyer
]

# === Tour Model ===
class Tour(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.FloatField()
    seats_available = models.IntegerField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('inactive','Inactive'),('active','Active')], default='inactive')

    def __str__(self):
        return self.name

    # Available seats after bookings
    def seats_remaining(self):
        total_booked = self.bookings.count()  # related_name from Booking
        return self.seats_available - total_booked

# === Hire / Subscription Model ===
class Hire(models.Model):
    user_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_admin.username} ({self.start_date} - {self.end_date})"

# === Booking / Enrollment Model ===
class Booking(models.Model):
    tour = models.ForeignKey(Tour, related_name="bookings", on_delete=models.CASCADE)
    enjoyer = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'role':'enjoyer'}, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    payment_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.enjoyer.username} -> {self.tour.name}"
