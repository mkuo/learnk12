from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.template.loader import get_template

from home.models import CourseReview
from home.models.courses_mixin import CoursesMixin
from home.models.util_models import ParamData


def courses(request):
    context = {}
    template = get_template('home/courses_table.html')
    context['sort_btn'] = CoursesMixin._get_course_sort_data(request, default_sort='-avg_score')

    # filtering
    context['filter_btns'] = {
        'tag': CoursesMixin._get_course_tag_data(request),
        'difficulty': CoursesMixin._get_course_difficulty_data(request),
        'provider': CoursesMixin._get_course_provider_data(request)
    }

    # courses
    context['courses_paged'], context['paging_data'] = CoursesMixin._get_courses_paged(
        ParamData.sanitize_int_arg(request, 'page', default=1),
        context['sort_btn'].selected_args[0],
        context['filter_btns']['tag'].selected_args,
        context['filter_btns']['difficulty'].selected_args,
        context['filter_btns']['provider'].selected_args
    )
    return template.render(context)


def course_reviews(request):
    review_query = CourseReview.objects.values(
        'score', 'publish_date', 'subject', 'description', 'reviewer_type', 'name', 'email', 'is_anonymous'
    )

    paginator = Paginator(review_query, per_page=1)
    try:
        reviews = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results
        page = paginator.num_pages
        reviews = paginator.page(page)

    reviews = list(reviews)
    for review in reviews:
        if review['is_anonymous']:
            del review['name']
            del review['email']
    return JsonResponse(reviews, safe=False)
