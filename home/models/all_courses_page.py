from wagtail.core.models import Page


class AllCoursesPage(Page):
    max_count = 1
    parent_page_type = ['HomePage']
    subpage_types = ['CourseSubjectPage']
