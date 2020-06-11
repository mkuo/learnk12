from django.db import models
from modelcluster.fields import ParentalKey
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

    panels = [ImageChooserPanel("image")]
