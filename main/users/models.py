from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_provider = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self._get_unique_slug()
            self.slug = slug
        super().save()

    def _get_unique_slug(self):
        unique_slug = get_random_string(length=8)
        while self.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug = get_random_string(length=8)
        return unique_slug


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
    start_time = models.TimeField(
        default=None, null=True, blank=True
    )
    end_time = models.TimeField(
        default=None, null=True, blank=True
    )

    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE,
        related_name='working_days'
    )


class Profile(models.Model):
    bio = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(
        max_length=15, blank=True, unique=True, null=True
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE,
        related_name='profile'
    )

    def __str__(self):
        return f'Profile of {self.user}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.user.is_provider:
            self.create_new_schedule(self.id)

    def create_new_schedule(self, profile_id):
        try:
            profile = WorkingDays.objects.filter(profile_id=profile_id).first()
        except WorkingDays.DoesNotExist:
            profile = None
        if not profile:
            days_list = []
            for day_code, label in WorkingDays.DayOfWeek.choices:
                days_list.append(
                    WorkingDays(day=day_code, profile=self)
                )
            WorkingDays.objects.bulk_create(days_list)