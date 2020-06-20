from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class LessonType(TaggedItemBase):
    content_object = ParentalKey(
        'CoursePage',
        on_delete=models.PROTECT,
    )


class Platform(TaggedItemBase):
    content_object = ParentalKey(
        'CoursePage',
        on_delete=models.PROTECT,
    )


class ProgrammingLanguage(TaggedItemBase):
    content_object = ParentalKey(
        'CoursePage',
        on_delete=models.PROTECT,
    )
