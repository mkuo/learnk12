from wagtail.core.models import Page

from home.submodels.course_detail_page import CourseDetailPage
from home.submodels.tutor_detail_page import TutorDetailPage


class HomePage(Page):
    max_count = 1
    parent_page_type = ['Page']

    def get_context(self, request):
        context = super().get_context(request)
        context['courses'] = Page.objects.type(CourseDetailPage)
        context['tutors'] = Page.objects.type(TutorDetailPage)
        return context
