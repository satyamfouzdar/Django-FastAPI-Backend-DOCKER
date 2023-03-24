from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractUser):
    """
    The user model
    """
    first_name = None
    last_name = None
    username = None
    name = models.CharField(max_length=255)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name', )

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Profile for Users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alternate_email = models.EmailField(_('alternate email address'), blank=True)
    phone_number = PhoneNumberField(blank=True)
    alternate_phone_number = PhoneNumberField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.email


class Employee(User):
    login_id = models.CharField(max_length=155, blank=True)
    employee_id = models.CharField(max_length=155, blank=True)
    onboarding_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.name