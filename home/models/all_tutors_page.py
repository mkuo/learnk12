from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Q
from wagtail.core.models import Page

from home.defs.enums import CourseSubject, TIMEZONE
from home.models import TutorPage
from home.models.util_models import ParamData, PagingData


class AllTutorsPage(Page):
    max_count = 1
    parent_page_type = ['HomePage']
    subpage_types = ['TutorPage']

    @staticmethod
    def _get_sort_data(request):
        sort_columns = {
            '-avg_score': 'Highest Rated',
            'title': 'Tutors Title (a-z)',
            'hourly_rate': 'Lowest Price',
        }
        return ParamData(request, 'sort', sort_columns, is_list=False, default='-avg_score')

    @staticmethod
    def _get_course_subjects(request):
        course_group = {value: value for value in CourseSubject.values}
        return ParamData(request, 'course', course_group)

    @staticmethod
    def _get_timezone(request):
        timezone_groups = {name: name for name, t in TIMEZONE}
        return ParamData(request, 'timezone', timezone_groups)

    def _get_tutors_paged(self, page, sort_arg, course_args, timezone_args, search_arg):
        tutor_query = TutorPage.objects.child_of(self).live().public()
        if sort_arg[0] == '-':
            tutor_query = tutor_query.order_by(F(sort_arg[1:]).desc(nulls_last=True))
        else:
            tutor_query = tutor_query.order_by(F(sort_arg).asc(nulls_last=True))

        course_filter = Q()
        for course in course_args:
            course_filter |= Q(course_subjects__icontains=course)
        tutor_query = tutor_query.filter(course_filter)
        timezone_filter = Q()
        for timezone in timezone_args:
            timezone_filter |= Q(timezone=timezone)

        tutor_query = tutor_query.filter(timezone_filter)

        if search_arg:
            search_filter = Q()
            search_filter |= Q(title__icontains=search_arg)
            search_filter |= Q(description__icontains=search_arg)
            tutor_query = tutor_query.filter(search_filter)
        paginator = Paginator(tutor_query, per_page=5)
        try:
            tutors = paginator.page(page)
        except EmptyPage:
            # if page is out of range (e.g. 9999), deliver last page of results
            page = paginator.num_pages
            tutors = paginator.page(page)

        paging_data = PagingData(page, paginator.num_pages, paginator.count)
        return tutors, paging_data

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request)

        # sorting
        context['sort_btn'] = self._get_sort_data(request)

        # filtering
        course_data = self._get_course_subjects(request)
        timezone_data = self._get_timezone(request)

        context['filter_btns'] = {
            ('course', 'Course'): course_data,
            ('timezone', 'Timezone'): timezone_data,
        }
        context['search'] = request.GET.get('search')

        context['tutors_paged'], context['paging_data'] = self._get_tutors_paged(
            ParamData.sanitize_int_arg(request, 'page', default=1),
            context['sort_btn'].selected_args[0],
            course_data.selected_args,
            timezone_data.selected_args,
            context['search'],
        )

        return context
