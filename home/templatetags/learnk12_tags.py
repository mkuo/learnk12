from collections import defaultdict
from django.template import Library
from urllib import parse

from home.submodels.course_detail_page import CourseDetailPage

register = Library()


@register.filter
def times(number):
    return range(number)


@register.filter
def course_difficulty_enum(text):
    return CourseDetailPage.CourseDifficulty(int(text)).label


@register.simple_tag
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


@register.simple_tag
def google_fonts_import_url():
    url = ("https://fonts.googleapis.com/css2?"
           "family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&"
           "family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&"
           "family=Material+Icons&"
           "family=Baloo+Bhaina+2&"
           "display=swap")
    return url


@register.simple_tag(takes_context=True)
def build_url(context, param, value):
    # parse the url
    url_string = context.request.get_full_path()
    url_parsed = parse.urlparse(url_string)
    url_query = parse.parse_qs(url_parsed.query)

    # build new query arguments
    new_query = defaultdict(list, url_query)

    if param == 'sort':
        desc_value = f'-{value}'
        if value in new_query[param]:
            # order was ascending, make descending
            idx = new_query[param].index(value)
            new_query[param][idx] = desc_value
        elif desc_value in new_query[param]:
            # order was descending, make neutral
            new_query[param].remove(desc_value)
        else:
            # order was neutral, make ascending
            new_query[param].append(value)
        # reset page when re-sorting
        new_query.pop('page', None)
    elif param in ['tag', 'difficulty', 'provider']:
        if value in new_query[param]:
            new_query[param].remove(value)
        else:
            new_query[param].append(value)
    else:
        # default behavior is to take last value
        new_query[param] = [value]

    # build new query
    encoded_query = parse.urlencode(new_query, doseq=True)
    return url_parsed._replace(query=encoded_query).geturl()