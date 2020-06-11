from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class CourseTag(TaggedItemBase):
    content_object = ParentalKey(
        'CoursePage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )
