from wagtail.core.models import Page


class AllBlogsPage(Page):
    max_count = 1
    parent_page_type = ['HomePage']
    subpage_types = ['BlogPage']
