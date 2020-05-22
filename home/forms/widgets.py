from django.forms.widgets import ChoiceWidget


class StarRatingWidget(ChoiceWidget):
    template_name = 'home/star_rating_form.html'
