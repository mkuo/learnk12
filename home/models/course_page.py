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

from home.defs.enums import CourseDifficulty, CostInterval
from home.forms.course_review_form import CourseReviewForm
from home.models.course_review import CourseReview
from home.models.course_tags import LessonType, Platform, ProgrammingLanguage
from home.models.util_models import ParamData, PagingData


class CoursePage(Page):
    # meta settings
    parent_page_type = ['CourseSubjectPage']
    subpage_types = []

    # database fields
    provider = models.ForeignKey('ProviderPage', blank=True, null=True, on_delete=models.SET_NULL)
    description = RichTextField(blank=True, null=True)
    course_url = models.URLField(blank=True, null=True)
    scheduled = models.BooleanField(blank=True, null=True)

    cost_amount = models.DecimalField(db_index=True, max_digits=9, decimal_places=2, blank=True, null=True)
    cost_interval = models.CharField(max_length=255, choices=CostInterval.choices, blank=True, null=True)

    age_low = models.PositiveSmallIntegerField(db_index=True, blank=True, null=True)
    age_high = models.PositiveSmallIntegerField(db_index=True, blank=True, null=True)

    lesson_count = models.PositiveSmallIntegerField(blank=True, null=True)
    lesson_length_minutes = models.PositiveSmallIntegerField(blank=True, null=True)
    course_length_hours = models.PositiveSmallIntegerField(db_index=True, blank=True, null=True)

    difficulty = models.PositiveSmallIntegerField(
        db_index=True, choices=CourseDifficulty.choices, blank=True, null=True
    )

    lesson_type_tags = ClusterTaggableManager(
        through=LessonType,
        blank=True,
        related_name='lesson_types',
        verbose_name='lesson types'
    )
    platform_tags = ClusterTaggableManager(
        through=Platform,
        blank=True,
        related_name='platforms',
        verbose_name='platforms'
    )
    programming_language_tags = ClusterTaggableManager(
        through=ProgrammingLanguage,
        blank=True,
        related_name='programming_languages',
        verbose_name='programming languages'
    )

    avg_score = models.FloatField(db_index=True, blank=True, null=True)
    review_count = models.IntegerField(default=0)

    # editor fields
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('provider'),
            FieldPanel('course_url'),
            FieldPanel('scheduled'),
        ], heading="details"),
        MultiFieldPanel([
            FieldPanel('cost_amount'),
            FieldPanel('cost_interval'),
        ], heading="cost"),
        MultiFieldPanel([
            FieldPanel('age_low'),
            FieldPanel('age_high'),
        ], heading="age"),
        MultiFieldPanel([
            FieldPanel('lesson_count'),
            FieldPanel('lesson_length_minutes'),
            FieldPanel('course_length_hours'),
            FieldPanel('difficulty'),
        ], heading="duration"),
        MultiFieldPanel([
            FieldPanel('lesson_type_tags'),
            FieldPanel('platform_tags'),
            FieldPanel('programming_language_tags'),
        ], heading="tags"),
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
                course_page_id=self.page_ptr_id,
                email=form.cleaned_data['email']
            ).exists()
            if existing_review:
                form.add_error('email', "A review already exists for this course and email.")
                context['form'] = form
                context['show_form'] = True
            else:
                obj = form.save(commit=False)
                obj.course_page_id = self.page_ptr_id
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