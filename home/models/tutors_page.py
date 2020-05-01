from wagtail.core.models import Page


class TutorsPage(Page):
    # meta settings
    slug = 'tutors'
    max_count = 1
    subpage_types = ['TutorDetailPage']
    parent_page_type = ['HomePage']
