from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.images.rect import Rect

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


@receiver(pre_save, sender=Image, dispatch_uid="pre_save_image_focus")
def pre_save_image_focus(sender, instance, **kwargs):
    if instance.focal_point_x is None and instance.focal_point_y is None:
        right = min(instance.width, 64)
        bottom = min(instance.height, 64)
        instance.set_focal_point(Rect(0, 0, right, bottom))
