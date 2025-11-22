from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.core.validators import MaxValueValidator

# Create your models here.

class TickModel(models.Model):

    date = models.DateTimeField(
        null=False,
        blank=False
    )

    location = models.CharField(
        max_length=30,
        null=False,
        blank=False
        )

    species = models.CharField(
        max_length=30,
        null=False,
        blank=False
    )

    latin_name = models.CharField(
        max_length=30,
        null=False,
        blank=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['location', 'date'],
                name='unique_location_to_time')]
    
    def __str__(self):
        return self.species + ", seen in " + self.location + " on date " + str(self.date.strftime('%d. %B %Y'))