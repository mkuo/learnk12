from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Q
from django.shortcuts import render, redirect
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from django.db import models

from home.defs.enums import CourseSubject, TIMEZONE
from home.forms.tutor_review_form import TutorReviewForm
from home.models.tutor_review import TutorReview
from home.models.util_models import ParamData, PagingData
from user_auth.models import User


class TutorPage(Page):
    # meta settings
    slug = 'tutor'
    subpage_types = ['TutorDetailPage']
    parent_page_type = ['AllTutorsPage']

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    course_subjects = models.CharField(max_length=255, choices=CourseSubject.choices, null=True, blank=False)
    is_accepting_students = models.BooleanField(null=True, blank=False)
    hourly_rate = models.PositiveIntegerField(null=True)
    timezone = models.CharField(max_length=255, choices=TIMEZONE, null=True)
    description = models.TextField(null=True)
    avg_score = models.FloatField(db_index=True, blank=True, null=True)
    review_count = models.IntegerField(default=0)
    public = models.BooleanField(default=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('user'),
        FieldPanel('course_subjects'),
        FieldPanel('is_accepting_students'),
        FieldPanel('hourly_rate'),
        FieldPanel('timezone'),
        FieldPanel('description'),
        FieldPanel('avg_score'),
    ]

    @property
    def override_title(self):
        return self.title + ' Reviews'

    @property
    def override_description(self):
        return BeautifulSoup(self.description, features='html5lib').get_text(' ', True)

    @staticmethod
    def _get_sort_data(request):
        sort_columns = {
            '-publish_date': 'Most Recent',
            '-score': 'Highest Rated'
        }
        return ParamData(request, 'sort', sort_columns, is_list=False, default='-publish_date')

    @staticmethod
    def _get_reviewer_type_data(request):
        diffs = {str(val): label for val, label in TutorReview.ReviewerType.choices}
        return ParamData(request, 'reviewer_type', diffs)

    def _get_reviews_pages(self, page, sort_arg, reviewer_type_args):
        # get reviews from database
        review_query = self.tutor_reviews
        if sort_arg[0] == '-':
            review_query = review_query.order_by(F(sort_arg[1:]).desc(nulls_last=True))
        else:
            review_query = review_query.order_by(F(sort_arg).asc(nulls_last=True))

        reviewer_type_filter = Q()
        for reviewer_type in reviewer_type_args:
            reviewer_type_filter |= Q(reviewer_type=reviewer_type)
        review_query = review_query.filter(reviewer_type_filter)

        paginator = Paginator(review_query, per_page=5)
        try:
            reviews = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            reviews = paginator.page(page)

        paging_data = PagingData(page, paginator.num_pages, paginator.count)
        return reviews, paging_data

    def get_context(self, request):
        context = super().get_context(request)

        # review sorting
        context['sort_btn'] = self._get_sort_data(request)

        # review filtering
        reviewer_type_data = self._get_reviewer_type_data(request)
        context['filter_btns'] = {
            ('reviewer_type', 'Reviewer Type'): reviewer_type_data
        }

        # query reviews
        context['anchor'] = 'reviews'
        context['reviews'], context['paging_data'] = self._get_reviews_pages(
            ParamData.sanitize_int_arg(request, 'page', default=1),
            context['sort_btn'].selected_args[0],
            reviewer_type_data.selected_args
        )
        user = request.user if request.user.is_authenticated else None
        context['form'] = TutorReviewForm(user=user)
        return context

    def append_to_reviewed_tutors(self, request):
        if 'reviewed_tutors' not in request.session:
            reviewed_tutors = []
        else:
            reviewed_tutors = request.session['reviewed_tutors']
        reviewed_tutors.append(self.page_ptr_id)
        request.session['reviewed_tutors'] = reviewed_tutors

    def process_form(self, request, context):
        user = request.user if request.user.is_authenticated else None
        form = TutorReviewForm(request.POST, user=user)
        do_redirect = False
        if form.is_valid():
            existing_review = TutorReview.objects.filter(
                tutor_page_id=self.page_ptr_id,
                email=form.cleaned_data['email']
            ).exists()
            if existing_review:
                form.add_error('email', "A review already exists for this course and email.")
                context['form'] = form
                context['show_form'] = True
            else:
                obj = form.save(commit=False)
                obj.tutor_page_id = self.page_ptr_id
                obj.user = request.user if request.user.is_authenticated else None
                obj.save()
                self.append_to_reviewed_tutors(request)
                do_redirect = True
        else:
            context['form'] = form
            context['show_form'] = True

        return do_redirect, request, context

    def serve(self, request):
        context = self.get_context(request)
        do_redirect = False
        if request.method == 'POST':
            do_redirect, request, context = self.process_form(request, context)
        if do_redirect:
            return redirect(self.url)
        else:
            return render(request, self.get_template(request), context)
