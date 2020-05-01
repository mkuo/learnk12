from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from wagtail.core.models import Page

from home.submodels.course_detail_page import CourseDetailPage
from home.submodels.course_tag import CourseTag


class CoursesPage(Page):
    # meta settings
    slug = 'courses'
    max_count = 1
    subpage_types = ['CourseDetailPage']
    parent_page_type = ['HomePage']

    sort_columns = [
        ('avg_score', 'Rating'),
        ('title', 'Title'),
        ('cost', 'Cost'),
        ('duration_hours', 'Duration')
    ]
    default_sort = 'avg_score'

    @staticmethod
    def _sanitize_args(request, param, allowed):
        args = request.GET.getlist(param, [])
        if not all(arg in allowed for arg in args):
            args = []
        return set(args)

    @staticmethod
    def _sanitize_page(request):
        default_page = 1
        page = request.GET.get('page', default_page)
        try:
            return int(page)
        except ValueError:
            return default_page

    def _get_sort_buttons(self, sort_args):
        sort_button_styling = {
            col: {
                'label': label,
                'button_color': 'btn-light',
                'material_icon': 'unfold_more'
            } for col, label in self.sort_columns
        }
        for column in sort_args:
            if column[0] == '-':
                col_key = column[1:]
                sort_button_styling[col_key]['material_icon'] = 'expand_more'
            else:
                col_key = column
                sort_button_styling[column]['material_icon'] = 'expand_less'
            sort_button_styling[col_key]['button_color'] = 'btn-primary'
        return sort_button_styling

    def _get_courses_paged(self, page, sort_args, tag_args, difficulty_args, provider_args):
        # get courses from database
        if not sort_args:
            sort_args = [self.default_sort]
        course_query = CourseDetailPage.objects.live().order_by(*sort_args)

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

    def _get_tags(self, request):
        results = CourseTag.objects.values('tag__slug', 'tag__name').distinct()
        tags = [(res['tag__slug'], res['tag__name']) for res in results]
        tag_args = self._sanitize_args(request, 'tag', [val for val, _ in tags])
        return tag_args, tags

    def _get_difficulties(self, request):
        difficulties = [(str(val), label) for val, label in CourseDetailPage.CourseDifficulty.choices]
        difficulty_args = self._sanitize_args(request, 'difficulty', [val for val, _ in difficulties])
        return difficulty_args, difficulties

    def _get_providers(self, request):
        results = CourseDetailPage.objects.live().order_by().values('provider').distinct()
        providers = [(res['provider'], res['provider']) for res in results]
        provider_args = self._sanitize_args(request, 'provider', [val for val, _ in providers])
        return provider_args, providers

    @staticmethod
    def _get_filter_buttons(args, choices):
        dropdown_btns = {
            choice[0]: {
                'label': choice[1],
                'btn_color': 'badge-white'
            } for choice in choices
        }
        for selection in args:
            dropdown_btns[selection]['btn_color'] = 'badge-primary'
        if args:
            main_btn = 'btn-primary'
        else:
            main_btn = 'btn-light'
        return {
            'dropdown_btns': dropdown_btns,
            'main_btn': main_btn,
            'select_count': len(args)
        }

    def get_context(self, request):
        context = super().get_context(request)

        sort_args = self._sanitize_args(
            request,
            'sort',
            [col for col, _ in self.sort_columns] + [f'-{col}' for col, _ in self.sort_columns]
        )
        context['sort_buttons'] = self._get_sort_buttons(sort_args)

        tag_args, tags = self._get_tags(request)
        difficulty_args, difficulties = self._get_difficulties(request)
        provider_args, providers = self._get_providers(request)
        context['filter_labels'] = {
            'tag': self._get_filter_buttons(tag_args, tags),
            'difficulty': self._get_filter_buttons(difficulty_args, difficulties),
            'provider': self._get_filter_buttons(provider_args, providers)
        }

        page = self._sanitize_page(request)
        context['courses_paged'] = self._get_courses_paged(
            page, sort_args, tag_args, difficulty_args, provider_args
        )

        return context
