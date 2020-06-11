from wagtail.core import blocks

from home.models import CoursePage


class CourseRankTableBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    link = blocks.PageChooserBlock(required=False)
    caption = blocks.CharBlock(required=False)
    filters = blocks.ListBlock(blocks.StructBlock([
        ('column', blocks.CharBlock()),
        ('value', blocks.CharBlock()),
    ]))
    excludes = blocks.ListBlock(blocks.StructBlock([
        ('column', blocks.CharBlock()),
        ('value', blocks.CharBlock()),
    ]))
    sorts = blocks.ListBlock(blocks.CharBlock())
    result_count = blocks.IntegerBlock()

    class Meta:
        template = 'home/course_rank_table.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        course_query = CoursePage.objects.live().public()
        if value['filters']:
            kwargs = {f['column']: f['value'] for f in value['filters']}
            course_query = course_query.filter(**kwargs)
        for e in value['excludes']:
            course_query = course_query.exclude(**{e['column']: e['value']})
        if value['sorts']:
            course_query = course_query.order_by(*value['sorts'])
        context['courses'] = course_query[:value['result_count']]
        return context
