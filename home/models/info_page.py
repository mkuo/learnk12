from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class InfoPage(Page):
    parent_page_type = ['HomePage']
    subpage_types = []
    info = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('info')
    ]
