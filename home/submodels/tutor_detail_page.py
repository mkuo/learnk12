from wagtail.core.models import Page

class TutorDetailPage(Page):
    # meta settings
    parent_page_type = ['TutorsPage']
    subpage_types = []