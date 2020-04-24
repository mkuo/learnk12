from django.db import models

from wagtail.core.models import Page

Page.subpage_types = ['home.HomePage']


class HomePage(Page):
    max_count = 1
    parent_page_type = ['Page']

    def get_context(self, request):
        context = super().get_context(request)
        context['courses'] = Page.objects.type(CourseDetailPage)
        context['tutors'] = Page.objects.type(TutorDetailPage)
        return context


class CoursesPage(Page):
    slug = 'courses'
    max_count = 1
    subpage_types = ['CourseDetailPage']
    parent_page_type = ['HomePage']


class CourseDetailPage(Page):
    parent_page_type = ['CoursesPage']
    subpage_types = []


class TutorsPage(Page):
    slug = 'tutors'
    max_count = 1
    subpage_types = ['TutorDetailPage']
    parent_page_type = ['HomePage']


class TutorDetailPage(Page):
    parent_page_type = ['TutorsPage']
    subpage_types = []
