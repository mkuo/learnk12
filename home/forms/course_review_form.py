from django.forms import ModelForm, Textarea, HiddenInput
from home.forms.widgets import StarRatingWidget
from home.models.course_review import CourseReview


class CourseReviewForm(ModelForm):
    class Meta:
        model = CourseReview
        fields = ['score', 'subject', 'description', 'reviewer_type', 'name', 'email']
        labels = {
            'reviewer_type': 'I am a'
        }
        help_texts = {
            'name': 'Your name is not shared.',
            'email': 'Your email is not shared.'
        }
        widgets = {
            'score': StarRatingWidget(choices=[(i, i) for i in range(1, 5)]),
            'subject': Textarea(attrs={'rows': 1}),
            'description': Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CourseReviewForm, self).__init__(*args, **kwargs)
        if not self.user:
            self.fields['name'].required = True
            self.fields['email'].required = True
        else:
            self.fields['name'].widget = HiddenInput()
            self.fields['email'].widget = HiddenInput()
