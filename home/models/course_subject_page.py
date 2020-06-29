from django.core.paginator import Paginator, EmptyPage
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Lower
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page

from home.defs.enums import AgeGroup, CourseDifficulty, CourseSubject
from home.models import CoursePage
from home.models.util_models import ParamData, PagingData


class CourseSubjectPage(Page):
    # meta settings
    subpage_types = ['CoursePage']
    parent_page_type = ['AllCoursesPage']

    heading = models.CharField(max_length=255)
    caption = models.TextField(blank=True, null=True)
    subject = models.CharField(db_index=True, max_length=255, choices=CourseSubject.choices)

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('caption'),
        FieldPanel('subject')
    ]

    @staticmethod
    def _get_sort_data(request):
        sort_columns = {
            '-avg_score': 'Highest Rated',
            'title': 'Course Title (a-z)',
            'cost_amount': 'Lowest Cost',
            'course_length_hours': 'Shortest Duration'
        }
        return ParamData(request, 'sort', sort_columns, is_list=False, default='-avg_score')

    @staticmethod
    def _get_course_age_data(request):
        age_groups = {name: AgeGroup[name].label for name in AgeGroup.names}
        return ParamData(request, 'age', age_groups)

    @staticmethod
    def _get_course_difficulty_data(request):
        diffs = {str(val): label for val, label in CourseDifficulty.choices}
        return ParamData(request, 'difficulty', diffs)

    def _get_course_provider_data(self, request):
        results = CoursePage.objects.child_of(self).live().public()\
            .order_by(Lower('provider__title')).values('provider__title').distinct()
        providers = {res['provider__title']: res['provider__title'] for res in results}
        return ParamData(request, 'provider', providers)

    def _get_courses_paged(self, page, sort_arg, age_args, difficulty_args, provider_args, search_arg):
        # get courses from database
        course_query = CoursePage.objects.child_of(self).live().public()
        if sort_arg[0] == '-':
            course_query = course_query.order_by(F(sort_arg[1:]).desc(nulls_last=True))
        else:
            course_query = course_query.order_by(F(sort_arg).asc(nulls_last=True))

        age_filter = Q()
        for age_group in age_args:
            low_filter, high_filter = AgeGroup[age_group].value
            low_q = (Q(age_low__lte=high_filter) | Q(age_low__isnull=True))
            high_q = (Q(age_high__gte=low_filter) | Q(age_high__isnull=True))
            age_filter |= Q(low_q, high_q)
        course_query = course_query.filter(age_filter)

        difficulty_filter = Q()
        for difficulty in difficulty_args:
            difficulty_filter |= Q(difficulty=difficulty)
        course_query = course_query.filter(difficulty_filter)

        provider_filter = Q()
        for provider_title in provider_args:
            provider_filter |= Q(provider__title=provider_title)
        course_query = course_query.filter(provider_filter)

        if search_arg:
            search_filter = Q()
            search_filter |= Q(title__icontains=search_arg)
            search_filter |= Q(description__icontains=search_arg)
            search_filter |= Q(provider__title__icontains=search_arg)
            course_query = course_query.filter(search_filter)

        paginator = Paginator(course_query, per_page=5)
        try:
            courses = paginator.page(page)
        except EmptyPage:
            # if page is out of range (e.g. 9999), deliver last page of results
            page = paginator.num_pages
            courses = paginator.page(page)

        paging_data = PagingData(page, paginator.num_pages, paginator.count)
        return courses, paging_data

    def get_context(self, request):
        context = super().get_context(request)

        # sorting
        context['sort_btn'] = self._get_sort_data(request)

        # filtering
        age_data = self._get_course_age_data(request)
        difficulty_data = self._get_course_difficulty_data(request)
        provider_data = self._get_course_provider_data(request)

        context['filter_btns'] = {
            ('age', 'Age'): age_data,
            ('difficulty', 'Difficulty'): difficulty_data,
            ('provider', 'Provider'): provider_data
        }
        context['search'] = request.GET.get('search')

        # query courses
        context['courses_paged'], context['paging_data'] = self._get_courses_paged(
            ParamData.sanitize_int_arg(request, 'page', default=1),
            context['sort_btn'].selected_args[0],
            age_data.selected_args,
            difficulty_data.selected_args,
            provider_data.selected_args,
            context['search']
        )
        return context
