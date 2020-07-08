from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=False)
    photo = models.ImageField(upload_to='images/profile/', null=False, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
