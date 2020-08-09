from bs4 import BeautifulSoup
from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from home.models import blocks
from home.models.course_rank_table import CourseRankTableBlock


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
        ('course_rank_table', CourseRankTableBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('publish_date'),
        SnippetChooserPanel("author"),
        ImageChooserPanel('main_image'),
        StreamFieldPanel("body"),
    ]

    @property
    def description(self):
        for stream_block in self.body:
            if stream_block.block_type == 'text':
                rich_text = stream_block.value.source
                return BeautifulSoup(rich_text, features='html5lib').get_text(' ', True)

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request)
        blogs = BlogPage.objects.live().public().\
            exclude(page_ptr_id=self.page_ptr_id).\
            order_by('-publish_date').\
            order_by('-last_published_at')[:3]
        context['recent_blogs'] = blogs
        return context


@register_snippet
class BlogAuthor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+"
    )
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
