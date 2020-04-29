from django.template import Library

register = Library()


@register.simple_tag
def google_fonts_import_url():
    url = ("https://fonts.googleapis.com/css2?"
           "family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&"
           "family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&"
           "family=Material+Icons&"
           "family=Baloo+Bhaina+2&"
           "display=swap")
    return url
