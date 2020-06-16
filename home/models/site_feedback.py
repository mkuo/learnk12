from django.db import models


class SiteFeedback(models.Model):
    category = models.TextField(db_index=True)
    description = models.TextField()
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "site feedback"
