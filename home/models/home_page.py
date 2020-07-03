from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from home.models.course_rank_table import CourseRankTableBlock


class HomePage(Page):
    max_count = 1
    parent_page_type = ['Page']
    subpage_types = [
        'AllCoursesPage',
        'AllProvidersPage',
        'InfoPage',
        'ProviderPage',
        'SiteFeedbackPage',
        'TutorsPage',
        'AllBlogsPage',
    ]
    heading = models.CharField(max_length=255)
    caption = models.TextField(blank=True, null=True)
    course_rank_tables = StreamField([
        ('course_rank_table', CourseRankTableBlock())
    ], blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('caption'),
        StreamFieldPanel('course_rank_tables'),
    ]
