from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock


class InfoPage(Page):
    parent_page_type = ['HomePage']
    subpage_types = []
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image_row', blocks.ListBlock(ImageChooserBlock())),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
