from bs4 import BeautifulSoup
from django.core.paginator import Paginator, EmptyPage
from django.db import models
from django.db.models import F, Q
from django.shortcuts import render, redirect
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from home.forms.course_review_form import CourseReviewForm
from home.models.course_review import CourseReview
from home.models.course_tag import CourseTag
from home.models.util_models import ParamData, PagingData


class CourseDetailPage(Page):
    # meta settings
    parent_page_type = ['CoursesPage']
    subpage_types = []

    class CourseDifficulty(models.IntegerChoices):
        # name to tuple of (value, age group)
        BEGINNER = (0, '5-7')
        EASY = (1, '8-10')
        MEDIUM = (2, '11-13')
        HARD = (3, '14-16')
        ADVANCED = (4, '17+')

    # database fields
    takeaway = models.TextField(blank=True, null=True)
    description = RichTextField()
    provider = models.CharField(db_index=True, max_length=255)
    course_url = models.URLField(blank=True, null=True)
    cost = models.DecimalField(db_index=True, max_digits=9, decimal_places=2)
    duration_hours = models.PositiveSmallIntegerField(db_index=True)
    difficulty = models.PositiveSmallIntegerField(db_index=True, choices=CourseDifficulty.choices)
    tags = ClusterTaggableManager(through=CourseTag, blank=True)
    avg_score = models.FloatField(db_index=True, blank=True, null=True)
    review_count = models.IntegerField(default=0)

    # editor fields
    content_panels = Page.content_panels + [
        FieldPanel('takeaway'),
        FieldPanel('description'),
        MultiFieldPanel(
            [
                FieldPanel('provider'),
                FieldPanel('course_url'),
                FieldPanel('cost'),
                FieldPanel('duration_hours'),
                FieldPanel('difficulty'),
                FieldPanel('tags')
            ],
            heading="Course Details"
        )
    ]

    image_panels = [
        InlinePanel('course_images', label="Images")
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(image_panels, heading='Images'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    @property
    def override_title(self):
        return self.title + ' Reviews'

    @property
    def override_description(self):
        return self.snippet

    @property
    def snippet(self):
        if self.takeaway:
            return self.takeaway
        else:
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
        diffs = {str(val): label for val, label in CourseReview.ReviewerType.choices}
        return ParamData(request, 'reviewer_type', diffs)

    def _get_reviews_pages(self, page, sort_arg, reviewer_type_args):
        # get reviews from database
        review_query = self.course_reviews
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
            # if page is out of range (e.g. 9999), deliver last page of results
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
        context['form'] = CourseReviewForm()
        return context

    def append_to_reviewed_courses(self, request):
        # append operations do not get saved to the request object
        # https://code.djangoproject.com/wiki/NewbieMistakes#Appendingtoalistinsessiondoesntwork
        if 'reviewed_courses' not in request.session:
            reviewed_courses = []
        else:
            reviewed_courses = request.session['reviewed_courses']
        reviewed_courses.append(self.page_ptr_id)
        request.session['reviewed_courses'] = reviewed_courses

    def process_form(self, request, context):
        form = CourseReviewForm(request.POST)
        do_redirect = False
        if form.is_valid():
            existing_review = CourseReview.objects.filter(
                course_detail_page_id=self.page_ptr_id,
                email=form.cleaned_data['email']
            ).exists()
            if existing_review:
                form.add_error('email', "A review already exists for this course and email.")
                context['form'] = form
                context['show_form'] = True
            else:
                obj = form.save(commit=False)
                obj.course_detail_page_id = self.page_ptr_id
                obj.save()
                self.append_to_reviewed_courses(request)
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
