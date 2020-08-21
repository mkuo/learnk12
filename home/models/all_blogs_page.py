from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page

from home import models as home_models
from django.db import models


class AllBlogsPage(Page):
    max_count = 1
    parent_page_type = ['HomePage']
    subpage_types = ['BlogPage']

    sub_heading = models.CharField(max_length=255, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('sub_heading')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(AllBlogsPage, self).get_context(request)
        all_resources = home_models.BlogPage.objects.live().public(). \
            order_by('-last_published_at').\
            order_by('-publish_date')
        paginator = Paginator(all_resources, 6)
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            resources = paginator.page(1)
        except EmptyPage:
            resources = paginator.page(paginator.num_pages)
        context['resources'] = resources
        return context
