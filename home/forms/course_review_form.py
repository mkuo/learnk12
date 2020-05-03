from django.forms import ModelForm, Textarea

from home.models.course_review import CourseReview


class CourseReviewForm(ModelForm):
    class Meta:
        model = CourseReview
        fields = ['score', 'subject', 'description', 'reviewer_type', 'name', 'email', 'is_anonymous']
        labels = {
            'reviewer_type': 'I am a',
            'is_anonymous': 'Review anonymously'
        }
        help_texts = {
            'name': 'Check the box below to hide your name',
            'email': 'Your email will not be shared'
        }
        widgets = {
            'subject': Textarea(attrs={'rows': 1}),
            'description': Textarea(attrs={'rows': 4}),
        }
