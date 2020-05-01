from wagtail.core.models import Page

from home.models.courses_mixin import CoursesMixin


class CoursesPage(CoursesMixin, Page):
    # meta settings
    slug = 'courses'
    max_count = 1
    subpage_types = ['CourseDetailPage']
    parent_page_type = ['HomePage']

    def get_context(self, request):
        context = super().get_context(request)

        # paging
        page = self._sanitize_int_arg(request, 'page', default=1)

        # sorting
        context['sort_btn'] = self._get_course_sort_data(request, default_sort='-avg_score')

        # filtering
        context['filter_btns'] = {
            'tag': self._get_course_tag_data(request),
            'difficulty': self._get_course_difficulty_data(request),
            'provider': self._get_course_provider_data(request)
        }

        context['courses_paged'] = self._get_courses_paged(
            page,
            context['sort_btn']['selected_arg'],
            context['filter_btns']['tag']['selected_args'],
            context['filter_btns']['difficulty']['selected_args'],
            context['filter_btns']['provider']['selected_args']
        )
        return context
