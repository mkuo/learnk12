from django.db import models
from django.db.models import TextField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock

Page.subpage_types = ['home.HomePage']


class HomePage(Page):
    max_count = 1
    parent_page_type = ['Page']

    def get_context(self, request):
        context = super().get_context(request)
        context['courses'] = Page.objects.type(CourseDetailPage)
        context['tutors'] = Page.objects.type(TutorDetailPage)
        return context


class CoursesPage(Page):
    # meta settings
    slug = 'courses'
    max_count = 1
    subpage_types = ['CourseDetailPage']
    parent_page_type = ['HomePage']

    def get_context(self, request):
        context = super().get_context(request)
        sort = request.GET['sort'] if 'sort' in request.GET else 'title'
        context['courses'] = CourseDetailPage.objects.live().order_by(sort).specific()
        return context


class CourseTag(TaggedItemBase):
    content_object = ParentalKey(
        'CourseDetailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


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
    summary = TextField(blank=True, null=True)
    overview = RichTextField()
    provider = models.CharField(max_length=255)
    course_url = models.CharField(max_length=2048, blank=True, null=True)
    cost = models.DecimalField(max_digits=9, decimal_places=2)
    duration_hours = models.PositiveSmallIntegerField()
    difficulty = models.PositiveSmallIntegerField(choices=CourseDifficulty.choices)
    tags = ClusterTaggableManager(through=CourseTag, blank=True)
    images = StreamField([
        ('image', ImageChooserBlock(required=False)),
    ], blank=True, null=True)

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
        ),
        StreamFieldPanel('images')
    ]

    def difficulty_label(self):
        return self.CourseDifficulty(self.difficulty).name


class TutorsPage(Page):
    # meta settings
    slug = 'tutors'
    max_count = 1
    subpage_types = ['TutorDetailPage']
    parent_page_type = ['HomePage']


class TutorDetailPage(Page):
    # meta settings
    parent_page_type = ['TutorsPage']
    subpage_types = []
