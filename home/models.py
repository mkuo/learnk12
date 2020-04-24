from django.db import models

from wagtail.core.models import Page


class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        context['courses'] = Page.objects.type(CourseDetailPage)
        return context


class CoursesPage(Page):
    pass


class CourseDetailPage(Page):
    pass
