from django.db import models

from user_auth.models import User


class SiteFeedback(models.Model):
    subject = models.TextField(db_index=True)
    description = models.TextField()
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "site feedback"
