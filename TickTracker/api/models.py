from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator

# Create your models here.

class TickModel(models.Model):

    date = models.DateTimeField(
        validators=[MaxValueValidator(datetime.now())],
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
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['location', 'date'],
                name='unique_title_in_artist')]
    
    def __str__(self):
        return self.species + ", seen in " + self.location + " on date " + str(self.date.strftime('%d. %B %Y'))

    def save(self, *args, **kwargs):
        self.latin_name = TickModel.objects.filter(species=self.species).values_list('latin_name', flat=True).distinct()[0]
        return super().save(*args, **kwargs)
