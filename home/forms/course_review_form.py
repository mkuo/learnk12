from django.forms import ModelForm, Textarea

from home.forms.widgets import StarRatingWidget
from home.models.course_review import CourseReview


class CourseReviewForm(ModelForm):
    class Meta:
        model = CourseReview
        fields = ['score', 'subject', 'description', 'reviewer_type', 'name', 'email', 'is_anonymous']
        labels = {
            'reviewer_type': 'I am a',
            'is_anonymous': 'Hide name and email'
        }
        help_texts = {
            'email': 'Your email is not shared in your review'
        }
        widgets = {
            'score': StarRatingWidget(choices=[(i, i) for i in range(1, 5)]),
            'subject': Textarea(attrs={'rows': 1}),
            'description': Textarea(attrs={'rows': 4}),
        }
