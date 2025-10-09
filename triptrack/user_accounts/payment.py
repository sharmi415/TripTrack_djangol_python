from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Hire(models.Model):
    user_admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'user_admin'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    paid = models.BooleanField(default=False)

    def duration_days(self):
        return (self.end_date - self.start_date).days
