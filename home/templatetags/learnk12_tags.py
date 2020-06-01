import re
from collections import defaultdict
from django.template import Library
from django.template.defaultfilters import pluralize
from urllib import parse
from home.models.course_detail_page import CourseDetailPage
from home.models.menu_item import MenuItem

register = Library()


@register.filter
def gr_than_eq(first, second):
    return first >= second


@register.filter
def is_in(el, iterable):
    return el in iterable


@register.filter
def eq(first, second):
    return first == second


@register.filter
def times(number):
    return range(number)


@register.filter
def course_difficulty_name(text):
    return CourseDetailPage.CourseDifficulty(int(text)).name


@register.filter
def course_difficulty_age(text):
    return CourseDetailPage.CourseDifficulty(int(text)).label


@register.filter
def get_stars(score):
    icons = []
    score = round(score * 2)
    for i in range(5):
        if score >= 2:
            icons.append('star')
        elif score >= 1:
            icons.append('star_half')
        else:
            icons.append('star_outline')
        score -= 2
    return icons


@register.filter
def minify_code(string):
    return re.sub('\n\s*', '', string).strip()


@register.simple_tag
def page_result_figures(paging_data, page=None):
    figures = '{} result{}'.format(
        paging_data.num_records,
        pluralize(paging_data.num_records)
    )
    if page:
        figures += ' from {} total review{}'.format(
            page.review_count,
            pluralize(page.review_count)
        )
    else:
        figures += ' returned'
    return figures


@register.simple_tag
def get_nav_menu():
    query = MenuItem.objects.exclude(title='footer').exclude(parent_item__title='footer')
    nested_menu_items = {}
    for item in query.filter(parent_item__isnull=True).order_by('order'):
        nested_menu_items[item] = []
    for item in query.filter(parent_item__isnull=False).order_by('order'):
        nested_menu_items[item.parent_item].append(item)
    return nested_menu_items


@register.simple_tag
def get_footer_menu():
    return MenuItem.objects.filter(parent_item__title='footer').order_by('order')


@register.simple_tag
def google_fonts_import_url():
    url = ("https://fonts.googleapis.com/css2?"
           "family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&"
           "family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&"
           "family=Material+Icons&"
           "display=swap")
    return url


@register.simple_tag(takes_context=True)
def build_url(context, param, value, multiple_vals=False):
    # parse the url
    url_string = context.request.get_full_path()
    url_parsed = parse.urlparse(url_string)
    url_query = parse.parse_qs(url_parsed.query)

    # build new query arguments
    new_query = defaultdict(list, url_query)

    if multiple_vals:
        if value in new_query[param]:
            # replace parameter if already exists
            new_query[param].remove(value)
        else:
            new_query[param].append(value)
    else:
        # take last of parameter
        new_query[param] = [value]

    if param != 'page':
        # reset page
        new_query.pop('page', None)

    # build new query
    encoded_query = parse.urlencode(new_query, doseq=True)
    return url_parsed._replace(query=encoded_query).geturl()
