from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, F

from home.models import CourseDetailPage, CourseTag
from home.models.util_models import ParamData, PagingData


class CoursesMixin:
    def _get_course_sort_data(self, request, default_sort):
        sort_column_labels = {
            '-avg_score': 'Rating',
            'title': 'Title',
            'cost': 'Cost',
            'duration_hours': 'Duration'
        }
        return ParamData(request, 'sort', sort_column_labels, is_list=False, default=default_sort)

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

        # get page numbers and parse for front-end
        range_start = max(page - 2, 1)
        range_stop = min(range_start + 5, paginator.num_pages + 1)
        paging_data = PagingData(range_start, range_stop, page, paginator.num_pages, paginator.count)

        return courses, paging_data
