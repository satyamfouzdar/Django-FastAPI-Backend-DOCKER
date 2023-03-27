from django.db import models


class Country(models.Model):
    """
    Model for Country
    """
    name = models.CharField(max_length=155)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name