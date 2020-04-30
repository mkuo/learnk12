from django.template import Library

from home.submodels.course_detail_page import CourseDetailPage

register = Library()


@register.filter
def course_difficulty_enum(text):
    return CourseDetailPage.CourseDifficulty(int(text)).label
