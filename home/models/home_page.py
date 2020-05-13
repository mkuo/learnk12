from wagtail.core.models import Page

from home.models.course_detail_page import CourseDetailPage


class HomePage(Page):
    max_count = 1
    parent_page_type = ['Page']

    def get_context(self, request):
        context = super().get_context(request)
        course_query = CourseDetailPage.objects.live().public()
        context['best_free'] = course_query.filter(cost=0).order_by('avg_score')[:3]
        context['highest_rated'] = course_query.order_by('avg_score')[:3]
        return context
