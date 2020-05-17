from django.db import models


class MenuItem(models.Model):
    title = models.CharField(null=True, blank=True, max_length=255)
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    parent_item = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title if self.title else ''

    def __unicode__(self):
        return self.title
