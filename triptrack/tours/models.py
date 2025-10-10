from django.db import models
from django.contrib.auth.models import User
from datetime import date

ROLE_CHOICES = [
    ('developer_admin', 'Developer Admin'),
    ('user_admin', 'User Admin'),
    ('user', 'User'),
]

class Tour(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.FloatField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('inactive','Inactive'),('active','Active')], default='inactive')

    def str(self):
        return self.name

class Hire(models.Model):
    user_admin = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    paid = models.BooleanField(default=False)