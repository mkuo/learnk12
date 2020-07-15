from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    class Meta:
        db_table = 'auth_user'

    birth_date = models.DateField(null=True, blank=False)
    photo = models.ImageField(upload_to='images/profile/', null=False, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
