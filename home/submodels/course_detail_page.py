from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from home.submodels.course_tag import CourseTag


class CourseDetailPage(Page):
    # meta settings
    parent_page_type = ['CoursesPage']
    subpage_types = []

    class CourseDifficulty(models.IntegerChoices):
        BEGINNER = 0
        EASY = 1
        MEDIUM = 2
        HARD = 3
        ADVANCED = 4

    # database fields
    summary = models.TextField(blank=True, null=True)
    overview = RichTextField()
    provider = models.CharField(db_index=True, max_length=255)
    course_url = models.CharField(max_length=2048, blank=True, null=True)
    cost = models.DecimalField(db_index=True, max_digits=9, decimal_places=2)
    duration_hours = models.PositiveSmallIntegerField(db_index=True)
    difficulty = models.PositiveSmallIntegerField(db_index=True, choices=CourseDifficulty.choices)
    tags = ClusterTaggableManager(through=CourseTag, blank=True)
    avg_score = models.FloatField(db_index=True, blank=True, null=True)

    # editor fields
    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        FieldPanel('overview'),
        MultiFieldPanel(
            [
                FieldPanel('provider'),
                FieldPanel('course_url'),
                FieldPanel('cost'),
                FieldPanel('duration_hours'),
                FieldPanel('difficulty'),
                FieldPanel('tags')
            ],
            heading="Course Details"
        )
    ]

    image_panels = [
        InlinePanel('course_images', label="Images")
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(image_panels, heading='Images'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request):
        context = super().get_context(request)
        context['reviews'] = self.course_reviews.all()
        return context
