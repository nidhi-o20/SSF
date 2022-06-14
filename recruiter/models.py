import email
from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
# from sqlalchemy import null

# Create your models here.

User = get_user_model()


class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    priority1 = models.CharField(max_length=50)
    priority2 = models.CharField(max_length=50)
    priority3 = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

