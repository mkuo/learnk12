from django.db import models


class SiteFeedback(models.Model):
    category = models.TextField(db_index=True)
    description = models.TextField()

    class SiteFeedbackStatus(models.TextChoices):
        SUBMITTED = 'submitted'
        RESOLVED = 'resolved'
        BACKLOG = 'backlog'
    status = models.CharField(
        choices=SiteFeedbackStatus.choices, max_length=24, default=SiteFeedbackStatus.SUBMITTED
    )
