from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel

from home.models.course_page import CoursePage


class CourseImage(Orderable):
    page = ParentalKey(
        CoursePage,
        on_delete=models.CASCADE,
        related_name='course_images'
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    caption = models.CharField(max_length=255)

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("caption")
    ]
