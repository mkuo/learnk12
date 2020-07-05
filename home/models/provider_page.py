from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class ProviderPage(Page):
    parent_page_type = ['AllProvidersPage']
    subpage_types = []

    description = RichTextField()
    provider_url = models.URLField(blank=True, null=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('provider_url'),
        ImageChooserPanel('logo'),
    ]