from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from wagtail.core.models import Page

from home.submodels.course_detail_page import CourseDetailPage


class CoursesPage(Page):
    # meta settings
    slug = 'courses'
    max_count = 1
    subpage_types = ['CourseDetailPage']
    parent_page_type = ['HomePage']

    sort_columns = ['title', 'cost', 'duration_hours']
    default_sort = 'title'

    @staticmethod
    def _sanitize_args(request, param, allowed):
        args = request.GET.getlist(param, [])
        if not all(col or f'-{col}' in allowed for col in args):
            args = []
        return args

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
                'label': col.split('_')[0],
                'button_color': 'btn-light',
                'material_icon': 'unfold_more'
            } for col in self.sort_columns
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

    def _get_courses_paged(self, page, sort_args, provider_args):
        # get courses from database
        if not sort_args:
            sort_args = [self.default_sort]
        course_query = CourseDetailPage.objects.live().order_by(*sort_args)
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

    def _get_providers(self, request):
        results = CourseDetailPage.objects.live().order_by().values('provider').distinct()
        providers = {result['provider'] for result in results}
        provider_args = self._sanitize_args(request, 'provider', providers)
        return provider_args, providers

    @staticmethod
    def _get_provider_buttons(provider_args, providers):
        filter_button_colors = {provider: 'badge-white' for provider in providers}
        for selected_provider in provider_args:
            filter_button_colors[selected_provider] = 'badge-primary'
        if provider_args:
            main_btn_color = 'btn-primary'
        else:
            main_btn_color = 'btn-light'
        return filter_button_colors, main_btn_color, len(provider_args)

    def get_context(self, request):
        context = super().get_context(request)

        sort_args = self._sanitize_args(request, 'sort', self.sort_columns)
        context['sort_buttons'] = self._get_sort_buttons(sort_args)

        provider_args, providers = self._get_providers(request)
        filter_button_colors, main_btn_color, select_count = self._get_provider_buttons(provider_args, providers)
        context['provider_dropdown_buttons'] = filter_button_colors
        context['provider_button_color'] = main_btn_color
        context['provider_select_count'] = select_count

        page = self._sanitize_page(request)
        context['courses_paged'] = self._get_courses_paged(page, sort_args, provider_args)

        return context
