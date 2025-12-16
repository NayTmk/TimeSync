from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import OneToOneField


# Create your models here.
class Profile(models.Model):
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(
        max_length=15, blank=True, unique=True
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.PROTECT,
        related_name='user'
    )


class Service(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=2)

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name='profile'
    )


class WorkingHours(models.Model):
    pass