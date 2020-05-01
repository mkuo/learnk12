from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, F

from home.models import CourseDetailPage, CourseTag


class CoursesMixin:
    def _get_course_sort_data(self, request, default_sort=None):
        sort_column_labels = {
            '-avg_score': 'Rating',
            'title': 'Title',
            'cost': 'Cost',
            'duration_hours': 'Duration'
        }
        sort_arg = self._sanitize_arg(request, 'sort', sort_column_labels.keys(), default_sort)
        return {
            'selected_arg': sort_arg,
            'selected_label': sort_column_labels[sort_arg],
            'choices': sort_column_labels
        }

    def _get_course_tag_data(self, request):
        results = CourseTag.objects.values('tag__slug', 'tag__name').distinct()
        tags = {res['tag__slug']: res['tag__name'] for res in results}
        tag_args = self._sanitize_args(request, 'tag', tags.keys())
        return {
            'selected_args': tag_args,
            'selected_labels': [tags[arg] for arg in tag_args],
            'choices': tags
        }

    def _get_course_difficulty_data(self, request):
        diffs = {str(val): label for val, label in CourseDetailPage.CourseDifficulty.choices}
        diff_args = self._sanitize_args(request, 'difficulty', diffs.keys())
        return {
            'selected_args': diff_args,
            'selected_labels': [diffs[arg] for arg in diff_args],
            'choices': diffs
        }

    def _get_course_provider_data(self, request):
        results = CourseDetailPage.objects.live().order_by().values('provider').distinct()
        providers = {res['provider']: res['provider'] for res in results}
        provider_args = self._sanitize_args(request, 'provider', providers.keys())
        return {
            'selected_args': provider_args,
            'selected_labels': [providers[arg] for arg in provider_args],
            'choices': providers
        }

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
        page_range = range(range_start, range_stop)

        return {
            'courses': courses,
            'page_range': page_range,
            'current_page': page,
            'num_pages': paginator.num_pages,
            'num_courses': paginator.count
        }

    @staticmethod
    def _sanitize_arg(request, param, allowed, default=None):
        arg = request.GET.get(param, default)
        if arg not in allowed:
            arg = default
        return arg

    @staticmethod
    def _sanitize_args(request, param, allowed):
        args = request.GET.getlist(param, [])
        if not all(arg in allowed for arg in args):
            args = []
        return set(args)

    @staticmethod
    def _sanitize_int_arg(request, param, default=None):
        page = request.GET.get(param, default)
        try:
            return int(page)
        except ValueError:
            return default
