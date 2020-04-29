from django.core.paginator import Paginator, EmptyPage
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

    @staticmethod
    def _sanitize_sort_args(request):
        default_sort = ['title']
        sort_args = request.GET.getlist('sort', default_sort)
        allowed_sort_columns = ['title', 'difficulty', 'provider', 'cost', 'duration_hours']
        if not all(col in allowed_sort_columns for col in sort_args):
            sort_args = default_sort
        return sort_args

    @staticmethod
    def _sanitize_page(request):
        default_page = 1
        page = request.GET.get('page', default_page)
        try:
            return int(page)
        except ValueError:
            return default_page

    @staticmethod
    def _get_sort_button_styling(sort_args):
        sort_columns = ['title', 'difficulty', 'provider', 'cost', 'duration_hours']
        sort_button_styling = {
            col: {
                'label': col.split('_')[0],
                'button_color': 'btn-light',  # default white
                'material_icon': 'unfold_more'
            } for col in sort_columns
        }
        for column in sort_args:
            if column[0] == '-':
                sort_button_styling[column[1:]]['button_color'] = 'btn-primary'
                sort_button_styling[column[1:]]['material_icon'] = 'expand_more'
            else:
                sort_button_styling[column]['button_color'] = 'btn-primary'
                sort_button_styling[column]['material_icon'] = 'expand_less'
        return sort_button_styling

    @staticmethod
    def _get_courses_paged(sort_args, page):
        # get courses from database
        course_query = CourseDetailPage.objects.live().order_by(*sort_args)
        paginator = Paginator(course_query, per_page=5)

        try:
            courses = paginator.page(page)
        except EmptyPage:
            # if page is out of range (e.g. 9999), deliver last page of results
            page = paginator.num_pages
            courses = paginator.page(page)

        # get page numbers and parse for front-end
        range_start = max(page - 2, 1)
        range_stop = min(range_start + 5, paginator.num_pages + 1)
        page_range = range(range_start, range_stop)

        return {
            'courses': courses,
            'page_range': page_range,
            'current_page': page,
            'num_pages': paginator.num_pages
        }

    def get_context(self, request):
        context = super().get_context(request)
        sort_args = self._sanitize_sort_args(request)
        page = self._sanitize_page(request)
        context['courses_paged'] = self._get_courses_paged(sort_args, page)
        context['sort_buttons'] = self._get_sort_button_styling(sort_args)
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
