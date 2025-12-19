from datetime import time
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_provider = models.BooleanField(default=False)


class WorkingDays(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = 'Mon', _('Monday')
        TUESDAY = 'Tue', _('Tuesday')
        WEDNESDAY = 'Wed', _('Wednesday')
        THURSDAY = 'Thu', _('Thursday')
        FRIDAY = 'Fri', _('Friday')
        SATURDAY = 'Sat', _('Saturday')
        SUNDAY = 'Sun', _('Sunday')

    day = models.CharField(
        max_length=3, choices=DayOfWeek,
        default=None, null=True
    )
    is_day_off = models.BooleanField(default=True)
    start_time = models.TimeField(default=time(9, 0))
    end_time = models.TimeField(default=time(18, 0))

    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE,
        related_name='working_days'
    )


class Profile(models.Model):
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(
        max_length=15, blank=True, unique=True
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.PROTECT,
        related_name='profile'
    )

    def __str__(self):
        return f'Profile of {self.user}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            self.create_new_schedule()

    def create_new_schedule(self):
        days_list = []
        for day_code, label in WorkingDays.DayOfWeek.choices:
            days_list.append(
                WorkingDays(day=day_code, profile=self)
            )
        WorkingDays.objects.bulk_create(days_list)