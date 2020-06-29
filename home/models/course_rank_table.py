from wagtail.core import blocks

from home.models import CoursePage


class CourseRankTableBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    link = blocks.PageChooserBlock(required=False)
    caption = blocks.CharBlock(required=False)
    courses = blocks.ListBlock(blocks.PageChooserBlock(page_type=CoursePage))

    class Meta:
        template = 'home/course_rank_table.html'
