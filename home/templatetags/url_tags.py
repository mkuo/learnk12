from collections import defaultdict
from django.template import Library
from urllib import parse

register = Library()


@register.simple_tag(takes_context=True)
def build_url(context, **kwargs):
    # parse the url
    url_string = context.request.get_full_path()
    url_parsed = parse.urlparse(url_string)
    url_query = parse.parse_qs(url_parsed.query)

    # build new query arguments
    new_query = defaultdict(list, url_query)
    for param, value in kwargs.items():
        if param == 'sort':
            desc_value = f'-{value}'
            if value in new_query[param]:
                # order was ascending, make descending
                idx = new_query[param].index(value)
                new_query[param][idx] = desc_value
            elif desc_value in new_query[param]:
                # order was descending, make neutral
                new_query[param].remove(desc_value)
                continue
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
