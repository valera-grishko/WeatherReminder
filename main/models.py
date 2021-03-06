from django.db import models
from datetime import timedelta
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Extended user model """

    notifications = models.BooleanField(default=True)
    period = models.DurationField(default=timedelta(hours=6))


class Follow(models.Model):
    """ Subscription model """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=40)
