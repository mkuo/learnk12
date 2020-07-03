from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from home.models import blocks


class BlogPage(Page):
    publish_date = models.DateField("Post date")
    author = models.ForeignKey("BlogAuthor", on_delete=models.SET_NULL, null=True, blank=True)
    main_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        related_name="+",
        on_delete=models.SET_NULL
    )
    body = StreamField([
        ('image', blocks.ImageBlock()),
        ('text', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        ImageChooserPanel('main_image'),
        StreamFieldPanel("body"),
        SnippetChooserPanel("author")
    ]


@register_snippet
class BlogAuthor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ForeignKey("wagtailimages.Image",
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name="+", )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ],
            heading="Name and Image",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"
