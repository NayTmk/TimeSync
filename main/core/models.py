from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


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


class Service(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=2)

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name='services'
    )


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
    is_day_of = models.BooleanField(default=True)
    start_time = models.TimeField(default='9:00')
    end_time = models.TimeField(default='18:00')

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name='working_days'
    )