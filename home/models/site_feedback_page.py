from html import unescape

from django.shortcuts import render, redirect
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from home.forms.site_feedback_form import SiteFeedbackForm


class SiteFeedbackPage(Page):
    max_count = 1
    parent_page_type = ['HomePage']
    subpage_types = []
    subheading = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('subheading'),
    ]

    def process_form(self, request, context):
        form = SiteFeedbackForm(request.POST)
        do_redirect = False
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            request.session['submitted_feedback'] = form.cleaned_data['category']
            do_redirect = True
        else:
            context['form'] = form
            context['show_form'] = True

        return do_redirect, request, context

    def get_context(self, request):
        context = super().get_context(request)
        subject = request.GET.get('subject')
        context['form'] = SiteFeedbackForm(
            initial={'subject': unescape(subject)}
        )
        return context

    def serve(self, request):
        context = self.get_context(request)
        do_redirect = False
        if request.method == 'POST':
            do_redirect, request, context = self.process_form(request, context)
        if do_redirect:
            return redirect(self.url)
        else:
            return render(request, self.get_template(request), context)
