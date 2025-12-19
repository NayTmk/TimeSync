from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=2)

    profile = models.ForeignKey(
        'users.Profile', on_delete=models.CASCADE,
        related_name='services'
    )