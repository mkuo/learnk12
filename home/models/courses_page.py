from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Q
from wagtail.core.models import Page

from home.models import CourseTag, CourseDetailPage
from home.models.util_models import ParamData, PagingData


class CoursesPage(Page):
    # meta settings
    slug = 'courses'
    max_count = 1
    subpage_types = ['CourseDetailPage']
    parent_page_type = ['HomePage']

    @staticmethod
    def _get_sort_data(request):
        sort_columns = {
            '-avg_score': 'Rating',
            'title': 'Title',
            'cost': 'Cost',
            'duration_hours': 'Duration'
        }
        return ParamData(request, 'sort', sort_columns, is_list=False, default='-avg_score')

    @staticmethod
    def _get_course_tag_data(request):
        results = CourseTag.objects.values('tag__slug', 'tag__name').distinct()
        tags = {res['tag__slug']: res['tag__name'] for res in results}
        return ParamData(request, 'tag', tags)

    @staticmethod
    def _get_course_difficulty_data(request):
        diffs = {str(val): label for val, label in CourseDetailPage.CourseDifficulty.choices}
        return ParamData(request, 'difficulty', diffs)

    @staticmethod
    def _get_course_provider_data(request):
        results = CourseDetailPage.objects.live().order_by().values('provider').distinct()
        providers = {res['provider']: res['provider'] for res in results}
        return ParamData(request, 'provider', providers)

    @staticmethod
    def _get_courses_paged(page, sort_arg, tag_args, difficulty_args, provider_args):
        # get courses from database
        course_query = CourseDetailPage.objects.live()
        if sort_arg[0] == '-':
            course_query = course_query.order_by(F(sort_arg[1:]).desc(nulls_last=True))
        else:
            course_query = course_query.order_by(F(sort_arg).asc(nulls_last=True))

        tag_filter = Q()
        for tag in tag_args:
            tag_filter |= Q(tags__slug=tag)
        course_query = course_query.filter(tag_filter).distinct()

        difficulty_filter = Q()
        for difficulty in difficulty_args:
            difficulty_filter |= Q(difficulty=difficulty)
        course_query = course_query.filter(difficulty_filter)

        provider_filter = Q()
        for provider in provider_args:
            provider_filter |= Q(provider=provider)
        course_query = course_query.filter(provider_filter)

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
        tag_data = self._get_course_tag_data(request)
        difficulty_data = self._get_course_difficulty_data(request)
        provider_data = self._get_course_provider_data(request)
        context['filter_btns'] = {
            ('tag', 'Tag'): tag_data,
            ('difficulty', 'Difficulty'): difficulty_data,
            ('provider', 'Provider'): provider_data
        }

        # query courses
        context['courses_paged'], context['paging_data'] = self._get_courses_paged(
            ParamData.sanitize_int_arg(request, 'page', default=1),
            context['sort_btn'].selected_args[0],
            tag_data.selected_args,
            difficulty_data.selected_args,
            provider_data.selected_args
        )
        return context
