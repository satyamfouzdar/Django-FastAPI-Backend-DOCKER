from django.db import models


class Country(models.Model):
    """
    Model for Country
    """
    name = models.CharField(max_length=155)
    shortcode = models.CharField(max_length=5)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Institution(models.Model):
    """
    Model for financial institutions
    """
    name = models.CharField(max_length=155)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    url = models.CharField(max_length=355)


    class Meta:
        verbose_name_plural = "Institutions"

    def __str__(self):
        return self.name